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
    branch_name = subprocess.check_output('git branch --show-current'.split()).decode().strip()
    without_prefix = branch_name[branch_name.index('/') + 1:]
    return without_prefix[:without_prefix.index('-')]


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
    branch_name = edit_using_vim('{}/{}-{}'.format(task_type, selected_issue.id, cleaned_title))

    subprocess.run(['git', 'checkout', '-b', branch_name, 'develop'])


def log_time(args):
    selected_issue = select_issue(user.issues) if args.select_issue else extract_issue_from_branch_name()
    spent_on = date.today() - timedelta(days=args.days_ago)
    redmine.time_entry.create(issue_id=selected_issue.id, hours=args.hours, spent_on=spent_on)


def show_issue(args):
    issue_from_current_branch = extract_issue_from_branch_name()
    url = '{}/issues/{}'.format(credentials['url'], issue_from_current_branch)
    subprocess.run(['firefox', url])


def review(args):
    issue_from_current_branch = extract_issue_from_branch_name()
    issue = redmine.issue.get(resource_id=issue_from_current_branch)
    issue.status_id = redmine.statuses['In review']
    issue.save()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_work = subparsers.add_parser('work')
parser_work.set_defaults(func=start_work)

parser_log_time = subparsers.add_parser('log-time')
parser_log_time.set_defaults(func=log_time)
parser_log_time.add_argument('--hours', default=8, help='Number of hours worked', dest='hours', type=int)
parser_log_time.add_argument('-d', default=0, help='Number of days ago', dest='days_ago', type=int)
parser_log_time.add_argument('-s', action='store_true', help='Run fzf to select issue', dest='select_issue')

parser_show_issue = subparsers.add_parser('show-issue')
parser_show_issue.set_defaults(func=show_issue)

parser_review = subparsers.add_parser('review')
parser_review.set_defaults(func=review)

args = parser.parse_args()
args.func(args)
