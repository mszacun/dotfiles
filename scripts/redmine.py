#!/usr/bin/env python3

import subprocess
import re
import sys
import argparse
from datetime import timedelta, date
from pathlib import Path

from redminelib import Redmine
import gitlab
import iterfzf

from pypass import PasswordStoreEntry


class MergeRequestDescription:
    def __init__(self, issue_type):
        self.mr_template = Path(f'.gitlab/merge_request_templates/{issue_type}.md').read_text()

    def with_issue_link(self, issue_link):
        lines = self.mr_template.splitlines()
        lines.insert(3, issue_link)
        return '\n'.join(lines)


class NoIssueInRedmineIssue:
    id = 0
    subject = '(tbd)'

    def save(self):
        pass


class StatusPrefetchingRedmine(Redmine):
    def __init__(self, *args, **kwargs):
        super(StatusPrefetchingRedmine, self).__init__(*args, **kwargs)

        self.statuses = {status.name: status for status in self.issue_status.all()}
        self.projects = {project.name: project for project in self.project.all()}
        self.trackers = {tracker.name: tracker for tracker in self.tracker.all()}


TEMPORARY_FILE_NAME = '/tmp/.redmine_text_edit'
BRANCH_NAME_REGEXP = re.compile('(?P<full>(?P<type>\w+)/(?P<issue>\d+)-(?P<text>.*))')
DEFAULT_NUMBER_OF_WORKING_HOURS = 8


def _get_credentials_from_password_store(pass_entry):
    output = subprocess.check_output(['pass', pass_entry]).decode().splitlines()
    result = {'password': output[0]}
    for line in output[1:]:
        if match := PASS_ADDITIONAL_ENTRY_REGEXP.match(line):
            result[match.group(1)] = match.group(2)

    return result


def edit_using_vim(text, filepath=TEMPORARY_FILE_NAME):
    with open(filepath, 'w') as f:
        f.write(text)

    subprocess.run(['vim', filepath])

    with open(filepath, 'r') as f:
        return f.read().strip()


def extract_issue_from_branch_name(branch_name=''):
    try:
        if not branch_name:
            branch_name = subprocess.check_output('git branch --show-current'.split()).decode().strip()
        return match.groupdict(default='') if (match := BRANCH_NAME_REGEXP.match(branch_name)) else {}
    except:
        return {}


def get_issue_redmine_link(issue):
    return '{}/issues/{}'.format(credentials['url'], issue)


def select_using_fzf(options, key=None):
    if not key:
        key = lambda option: str(option)

    str_options = list(map(key, options))

    selected_option = iterfzf.iterfzf(str_options)
    index = str_options.index(selected_option)
    return options[index]


def select_issue(issues):
    return select_using_fzf(list(issues), lambda issue: f'{issue.id} - {issue.subject}')


credentials = PasswordStoreEntry('identt/redmine')
gitlab_credentials = PasswordStoreEntry('gitlab/api_token')

redmine = StatusPrefetchingRedmine(credentials['url'], username=credentials['login'], password=credentials['password'])
user = redmine.user.get(resource_id=credentials['user_id'])
gitlab = gitlab.Gitlab('https://gitlab.com/', private_token=gitlab_credentials['password'])
gitlab.auth()


def start_work(args):
    selected_issue = select_issue(list(user.issues) + [NoIssueInRedmineIssue()])
    task_type = select_using_fzf(['feature', 'bug', 'chore', 'refactor', 'test', 'devops', 'docs'])
    cleaned_title = selected_issue.subject.replace('-', '').replace(' ', '-').lower()
    branch_name = edit_using_vim('{}/{}-{}'.format(task_type, selected_issue.id, cleaned_title)).strip()

    subprocess.run(['git', 'fetch'])
    subprocess.run(['git', 'checkout', '-b', branch_name, 'origin/develop'])
    subprocess.run(['timew', 'start', branch_name])

    selected_issue.status_id = redmine.statuses['In progress'].id
    selected_issue.save()


def log_time(args):
    selected_issue = args.issue or select_issue(user.issues).id
    spent_on = date.today() - timedelta(days=args.days_ago)

    already_spent_hours = sum(r.hours for r in redmine.time_entry.filter(spent_on=spent_on, user_id=user.id))
    reaming_hours = DEFAULT_NUMBER_OF_WORKING_HOURS - already_spent_hours
    hours = args.hours or reaming_hours

    redmine.time_entry.create(issue_id=selected_issue, hours=hours, spent_on=spent_on, comments=args.comment)


def show_issue(args):
    subprocess.run(['firefox', get_issue_redmine_link(extract_issue_from_branch_name().get('issue'))])


def review(args):
    temporary_file = '/tmp/.mr.md'
    issue_from_current_branch = extract_issue_from_branch_name()
    issue = redmine.issue.get(resource_id=issue_from_current_branch['issue']) if issue_from_current_branch['issue'] != '0' else NoIssueInRedmineIssue()
    issue.status_id = redmine.statuses['In review'].id
    issue.save()

    project = gitlab.projects.get(gitlab_credentials['i2c'])
    issue_link = get_issue_redmine_link(issue_from_current_branch['issue'])
    mr_template = args.template or issue_from_current_branch['type']
    mr_text = edit_using_vim(MergeRequestDescription(mr_template).with_issue_link(issue_link), temporary_file)
    last_commit = subprocess.check_output('git show -s --format=%s'.split()).decode().strip()
    labels = [iterfzf.iterfzf(['Patch', 'Minor', 'Major'])] + [iterfzf.iterfzf(['S', 'M', 'L'])]

    mr = project.mergerequests.create({'source_branch': issue_from_current_branch['full'],
                                       'target_branch': 'develop',
                                       'title': last_commit,
                                       'labels': labels,
                                       'description': mr_text,
                                       'remove_source_branch': True,
                                       'squash': True,
                                       'assignee_id': gitlab.user.id})
    print(mr.web_url)


def mark_tested(args):
    project = gitlab.projects.get(gitlab_credentials['i2c'])
    untested_mrs = [mr for mr in project.mergerequests.list(state='merged', assignee_id=gitlab.user.id) if not 'Tested' in mr.labels]
    mr_to_mark = select_using_fzf(untested_mrs, key=lambda mr: mr.title)
    mr_to_mark.labels += ['Tested']
    mr_to_mark.save()

    issue_from_current_branch = extract_issue_from_branch_name(mr_to_mark.source_branch)
    issue = redmine.issue.get(resource_id=issue_from_current_branch['issue']) if issue_from_current_branch['issue'] != '0' else NoIssueInRedmineIssue()
    issue.status_id = redmine.statuses['Closed'].id
    issue.save()


def commit(args):
    branch_info = extract_issue_from_branch_name()
    issue = redmine.issue.get(resource_id=branch_info['issue']) if branch_info['issue'] != '0' else NoIssueInRedmineIssue()
    task_type = branch_info['type']

    commit_template = '{}: {} #{}'.format(task_type.capitalize(), issue.subject, branch_info['issue'])
    subprocess.run(['git', 'commit', '-v', '-e', '-m', commit_template])


def create_issue(args):
    return redmine.issue.create(
        project_id=select_using_fzf(list(redmine.projects.values()), key=lambda p: p.name).id,
        subject=edit_using_vim('Enter issue subject'),
        description=edit_using_vim('Enter issue description'),
        tracker_id=select_using_fzf(list(redmine.trackers.values()), key=lambda t: t.name).id,
        custom_fields=[{'id': 6, 'name': 'activity area', 'multiple': True, 'value': ['backend']}],
        assigned_to_id=user.id,
    )


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_work = subparsers.add_parser('work')
parser_work.set_defaults(func=start_work)

parser_log_time = subparsers.add_parser('log-time')
parser_log_time.set_defaults(func=log_time)
parser_log_time.add_argument('--hours', default=None, help='Number of hours worked, leave empty to calculate reaming hours for given day', dest='hours', type=float)
parser_log_time.add_argument('-d', default=0, help='Number of days ago', dest='days_ago', type=int)
parser_log_time.add_argument('--comment', help='Time entry comment', dest='comment')
parser_log_time.add_argument('--select-issue', action='store_const', help='Run fzf to select issue', dest='issue', const=None)
parser_log_time.add_argument('--issue-from-branch', action='store_const', help='Extract issue from branch name', dest='issue', const=extract_issue_from_branch_name().get('issue'))
parser_log_time.add_argument('--architecture', action='store_const', help='Log hours for architecture meeting', dest='issue', const=credentials['agile_meeting_issue'])
parser_log_time.add_argument('--planning', action='store_const', help='Log hours for plannig meeting', dest='issue', const=credentials['planning_meeting_issue'])
parser_log_time.add_argument('--superidentt', action='store_const', help='Log hours for superidentt tasks', dest='issue', const=credentials['superidentt_issue'])

parser_show_issue = subparsers.add_parser('show-issue')
parser_show_issue.set_defaults(func=show_issue)

parser_review = subparsers.add_parser('review')
parser_review.set_defaults(func=review)
parser_review.add_argument('-t', dest='template', help='Template path', default=None)

parser_commit = subparsers.add_parser('commit')
parser_commit.set_defaults(func=commit)

parser_commit = subparsers.add_parser('create-issue')
parser_commit.set_defaults(func=create_issue)

parser_mark_tested = subparsers.add_parser('mark-tested')
parser_mark_tested.set_defaults(func=mark_tested)

args = parser.parse_args()
args.func(args)
