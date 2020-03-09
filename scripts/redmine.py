#!/usr/bin/env python3

import subprocess
import re
import sys
import argparse

from redminelib import Redmine
import iterfzf



PASS_ADDITIONAL_ENTRY_REGEXP = re.compile('(\w+): (.*)')


def _get_credentials_from_password_store(pass_entry):
    output = subprocess.check_output(['pass', pass_entry]).decode().splitlines()
    result = {'password': output[0]}
    for line in output[1:]:
        if match := PASS_ADDITIONAL_ENTRY_REGEXP.match(line):
            result[match.group(1)] = match.group(2)

    return result


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

redmine = Redmine(credentials['url'], username=credentials['login'], password=credentials['password'])
user = redmine.user.get(resource_id=credentials['user_id'])


def start_work(args):
    selected_issue = select_issue(user.issues)
    task_type = select_using_fzf(['feature', 'bug'])
    branch_name = '{}/{}-{}'.format(task_type, selected_issue.id, selected_issue.subject.replace('-', '').replace(' ', '-').lower())

    subprocess.run(['git', 'checkout', '-b', branch_name, 'develop'])


def log_time(args):
    selected_issue = select_issue(user.issues)
    redmine.time_entry.create(issue_id=selected_issue.id, hours=8)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_work = subparsers.add_parser('work')
parser_work.set_defaults(func=start_work)

parser_work = subparsers.add_parser('log_time')
parser_work.set_defaults(func=log_time)

args = parser.parse_args()
args.func(args)


