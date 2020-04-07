#!/usr/bin/env python3

import subprocess
import re
import sys
import argparse
from datetime import timedelta, date

from redminelib import Redmine
import iterfzf


class StatusPrefetchingRedmine(Redmine):
    def __init__(self, *args, **kwargs):
        super(StatusPrefetchingRedmine, self).__init__(*args, **kwargs)

        self.statuses = {status.name: status for status in self.issue_status.all()}


PASS_ADDITIONAL_ENTRY_REGEXP = re.compile('(\w+): (.*)')
TEMPORARY_FILE_NAME = '/tmp/.redmine_text_edit'
BRANCH_NAME_REGEXP = re.compile('(?P<type>\w+)/(?P<issue>\d+)-(?P<text>.*)')


def _get_credentials_from_password_store(pass_entry):
    output = subprocess.check_output(['pass', pass_entry]).decode().splitlines()
    result = {'password': output[0]}
    for line in output[1:]:
        if match := PASS_ADDITIONAL_ENTRY_REGEXP.match(line):
            result[match.group(1)] = match.group(2)

    return result


def edit_using_vim(text):
    with open(TEMPORARY_FILE_NAME, 'w') as f:
        f.write(text)

    subprocess.run(['vim', TEMPORARY_FILE_NAME])

    with open(TEMPORARY_FILE_NAME, 'r') as f:
        return f.read()


def extract_issue_from_branch_name():
    try:
        branch_name = subprocess.check_output('git branch --show-current'.split()).decode().strip()
        return match.groupdict(default='') if (match := BRANCH_NAME_REGEXP.match(branch_name)) else {}
    except:
        return {}


def select_using_fzf(options, key=None):
    if not key:
        key = lambda option: str(option)

    str_options = list(map(key, options))

    selected_option = iterfzf.iterfzf(str_options)
    index = str_options.index(selected_option)
    return options[index]


def select_issue(issues):
    return select_using_fzf(list(issues), lambda issue: f'{issue.id} - {issue.subject}')


credentials = _get_credentials_from_password_store('identt/redmine')

redmine = StatusPrefetchingRedmine(credentials['url'], username=credentials['login'], password=credentials['password'])
user = redmine.user.get(resource_id=credentials['user_id'])


def start_work(args):
    selected_issue = select_issue(user.issues)
    task_type = select_using_fzf(['feature', 'bug', 'chore', 'refactor'])
    cleaned_title = selected_issue.subject.replace('-', '').replace(' ', '-').lower()
    branch_name = edit_using_vim('{}/{}-{}'.format(task_type, selected_issue.id, cleaned_title)).strip()

    subprocess.run(['git', 'fetch'])
    subprocess.run(['git', 'checkout', '-b', branch_name, 'origin/develop'])

    selected_issue.status_id = redmine.statuses['In progress'].id
    selected_issue.save()


def log_time(args):
    selected_issue = args.issue or select_issue(user.issues).id
    spent_on = date.today() - timedelta(days=args.days_ago)
    redmine.time_entry.create(issue_id=selected_issue, hours=args.hours, spent_on=spent_on, comments=args.comment)


def show_issue(args):
    issue_from_current_branch = extract_issue_from_branch_name().get('issue')
    url = '{}/issues/{}'.format(credentials['url'], issue_from_current_branch)
    subprocess.run(['firefox', url])


def review(args):
    issue_from_current_branch = extract_issue_from_branch_name().get('issue')
    issue = redmine.issue.get(resource_id=issue_from_current_branch)
    issue.status_id = redmine.statuses['In review'].id
    issue.save()


def commit(args):
    branch_info = extract_issue_from_branch_name()
    issue = redmine.issue.get(resource_id=branch_info['issue'])
    task_type = branch_info['type']

    commit_template = '{}: {} #{}'.format(task_type.capitalize(), issue.subject, branch_info['issue'])
    subprocess.run(['git', 'commit', '-e', '-m', commit_template])


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_work = subparsers.add_parser('work')
parser_work.set_defaults(func=start_work)

parser_log_time = subparsers.add_parser('log-time')
parser_log_time.set_defaults(func=log_time)
parser_log_time.add_argument('--hours', default=8, help='Number of hours worked', dest='hours', type=float)
parser_log_time.add_argument('-d', default=0, help='Number of days ago', dest='days_ago', type=int)
parser_log_time.add_argument('--comment', help='Time entry comment', dest='comment')
parser_log_time.add_argument('--select-issue', action='store_const', help='Run fzf to select issue', dest='issue', const=None)
parser_log_time.add_argument('--issue-from-branch', action='store_const', help='Extract issue from branch name', dest='issue', const=extract_issue_from_branch_name().get('issue'))
parser_log_time.add_argument('--architecture', action='store_const', help='Log hours for architecture meeting', dest='issue', const=credentials['agile_meeting_issue'])
parser_log_time.add_argument('--planning', action='store_const', help='Log hours for plannig meeting', dest='issue', const=credentials['planning_meeting_issue'])

parser_show_issue = subparsers.add_parser('show-issue')
parser_show_issue.set_defaults(func=show_issue)

parser_review = subparsers.add_parser('review')
parser_review.set_defaults(func=review)

parser_commit = subparsers.add_parser('commit')
parser_commit.set_defaults(func=commit)

args = parser.parse_args()
args.func(args)
