from __future__ import (unicode_literals, division, absolute_import, print_function)
import os
import re

from powerline.lib.threaded import ThreadedSegment
from jenkinsapi.jenkins import Jenkins


class JenkinsJobStatus(object):
    running = False

    def show_notification(self, job_name):
        pass

    def get_progress(self):
        return ''


class JenkinsRunningJobStatus(JenkinsJobStatus):
    running = True

    def __init__(self, completed_tests_number, all_tests_number):
        self.completed_tests_number = completed_tests_number
        self.all_tests_number = all_tests_number

    def show_notification(self, job_name):
        notification = '"Job {} is starting"'.format(job_name)
        os.system('notify-send {}'.format(notification))

    def get_progress(self):
        progress = None

        if self.completed_tests_number and self.all_tests_number:
            progress = int(100 * self.completed_tests_number / float(self.all_tests_number))
        else:
            progress = '?'

        return '{}%'.format(progress)


class JenkinsGoingToFailJobStatus(JenkinsRunningJobStatus):
    good = False

    def show_notification(self, job_name):
        notification = '"Job {} is going to fail"'.format(job_name)
        os.system('notify-send -u critical {}'.format(notification))


class JenkinsSoFarOKStatus(JenkinsRunningJobStatus):
    good = True


class JenkinsFailedStatus(JenkinsJobStatus):
    good = False

    def show_notification(self, job_name):
        notification = '"Job {} has failed"'.format(job_name)
        os.system('notify-send -u critical {}'.format(notification))


class JenkinsPassedStatus(JenkinsJobStatus):
    good = True

    def show_notification(self, job_name):
        notification = '"Job {} has end successfully"'.format(job_name)
        os.system('notify-send {}'.format(notification))

class JenkinsSegment(ThreadedSegment):
    interval = 30
    blink_state = 0
    ok_icon = u'\uF118'
    fail_icon = u'\uF119'
    working_icon = u'\ue799'
    JENKINS_URL = 'http://wrling31.emea.nsn-net.net:9090'
    FAILED_TEST_MARKER = 'F'
    ERROR_TEST_MARKER = 'E'

    def __init__(self, *args, **kwargs):
        self.job_name = kwargs.pop('job_name')
        self.verbose_name = kwargs.pop('verbose_name', self.job_name)

        super(JenkinsSegment, self).__init__(*args, **kwargs)

    def get_running_build_status(self, build):
        console_text = build.get_console()
        test_results_start_index = console_text.find('collected')

        if test_results_start_index == -1:
            return JenkinsSoFarOKStatus(None, None)

        test_results_text = console_text[test_results_start_index:]
        completed_tests_number = self._get_number_of_completed_tests(test_results_text)
        all_tests_number = self._get_number_of_all_tests(test_results_text)

        if  self._is_going_to_fail(test_results_text):
            return JenkinsGoingToFailJobStatus(completed_tests_number, all_tests_number)
        else:
            return JenkinsSoFarOKStatus(completed_tests_number, all_tests_number)

    def get_build_status(self, job_name):
        jenkins = Jenkins(self.JENKINS_URL)

        job = jenkins.get_job(job_name)
        build = job.get_last_build()

        if build.is_running():
            return self.get_running_build_status(build)
        else:
            return JenkinsPassedStatus() if build.is_good() else JenkinsFailedStatus()

    def _is_going_to_fail(self, test_results_text):
        return (test_results_text.find(self.FAILED_TEST_MARKER) != -1 or
             test_results_text.find(self.ERROR_TEST_MARKER) != -1)

    def _get_number_of_all_tests(self, test_results_text):
        return re.match(r'collected (\d+) items', test_results_text).group(1)

    def _get_number_of_completed_tests(self, test_results_text):
        first_test_file_offset = 2
        tests_number = 0

        for test_file_result in test_results_text.split('\n')[first_test_file_offset:]:
            tests_number += self._count_tests_in_file(test_file_result)

        return tests_number

    def _count_tests_in_file(self, test_file_result):
        after_space_position = test_file_result.find(' ') + 1
        tests_results = test_file_result[after_space_position:]

        return len(tests_results)

    def update(self, old_value):
        new_value = self.get_build_status(self.job_name)

        if type(new_value) != type(old_value):
            new_value.show_notification(self.job_name)

        return new_value

    def render(self, job_status, **kwargs):
        highlight_groups = []
        content = None

        self.blink_state = (self.blink_state + 1) % 2
        icon = self.ok_icon if job_status.good else self.fail_icon
        if job_status.running:
            highlight_groups.append('working_' + ('ok' if job_status.good else 'fail'))

        icon = ' ' if self.blink_state and job_status.running else icon
        progress = job_status.get_progress()

        if progress:
            content = '{} {} {}'.format(icon, progress, self.verbose_name)
        else:
            content = '{} {}'.format(icon, self.verbose_name)

        result = {'contents': content}
        if highlight_groups:
            result['highlight_groups'] = highlight_groups

        return [result]

ft = JenkinsSegment(job_name='aginoodle_FT', verbose_name='FT')
mt = JenkinsSegment(job_name='aginoodle_MT', verbose_name='MT')
ut = JenkinsSegment(job_name='aginoodle_UT', verbose_name='UT')
