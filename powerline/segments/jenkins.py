from __future__ import (unicode_literals, division, absolute_import, print_function)
import os
import re

from powerline.lib.threaded import ThreadedSegment
from jenkinsapi.jenkins import Jenkins


class InJobFileValue(object):
    def __init__(self, file_suffix, default_value=None):
        self.default_value = default_value
        self.file_suffix = file_suffix

    def __get__(self, instance, owner):
        if os.path.exists(self._file_path(instance)):
            with open(self._file_path(instance), 'r') as value_file:
                return value_file.read().strip()
        else:
            return self.default_value

    def __set__(self, instance, value):
        with open(self._file_path(instance), 'w') as value_file:
            value_file.write(str(value))

    def _file_path(self, instance):
        return os.path.join(os.environ['HOME'], '.{}.{}'.format(instance.job_name, self.file_suffix))


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
            progress = unicode(int(100 * self.completed_tests_number / float(self.all_tests_number)))
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
    interval = 300
    JENKINS_URL = 'http://wrling31.emea.nsn-net.net:9090'

    def __init__(self, *args, **kwargs):
        self.job_name = kwargs.pop('job_name')

        super(JenkinsSegment, self).__init__(*args, **kwargs)

    def update(self, old_value):
        build = self._get_last_build(self.job_name)
        new_value = self._get_build_status(build)

        if type(new_value) != type(old_value):
            new_value.show_notification(self.job_name)

        return new_value

    def _get_last_build(self, job_name):
        jenkins = Jenkins(self.JENKINS_URL)

        job = jenkins.get_job(job_name)
        return job.get_last_build()


class DonePylintJobStatus(JenkinsJobStatus):
    def __init__(self, number_of_warnings):
        self.number_of_warnings = number_of_warnings


class PylintJenkinsSegment(JenkinsSegment):
    PYTHON_ICON = u'\uE73C'
    MINUS_ICON = u'\uF4A3'
    UP_ICON = u'\uF176'
    DOWN_ICON = u'\uf175'

    WARNING_REGEX = re.compile(
        r'\[WARNINGS\] Successfully parsed file .* with (\d+) unique warnings and \d+ duplicates.')

    _previous_warnings_number = InJobFileValue('previous_warnings_number', 0)
    _current_warnings_number = InJobFileValue('current_warnings_number', 0)
    _current_build_number = InJobFileValue('current_build_number', 0)

    def render(self, job_status, *args, **kwargs):
        return [{'contents': '{icon} {number_of_warnings} {trend_icon}'.format(
            icon=self.PYTHON_ICON,
            number_of_warnings=job_status.number_of_warnings,
            trend_icon=self._get_trend_icon())}]

    def _get_build_status(self, build):
        if not build.is_running():
            job_status = DonePylintJobStatus(self._parse_number_of_pylint_warnings(build))

            if build.buildno != self._current_build_number:
                self._current_build_number = build.buildno
                self._previous_warnings_number = self._current_warnings_number
                self._current_warnings_number = job_status.number_of_warnings

                return job_status
        else:
            return JenkinsJobStatus()

    def _parse_number_of_pylint_warnings(self, build):
        console_text = build.get_console()
        return self.WARNING_REGEX.search(console_text).group(1)

    def _get_trend_icon(self):
        current_warnings_number = int(self._current_warnings_number)
        previous_warnings_number = int(self._previous_warnings_number)

        if current_warnings_number > previous_warnings_number:
            return self.UP_ICON
        if current_warnings_number < previous_warnings_number:
            return self.DOWN_ICON
        return self.MINUS_ICON


class PyTestJenkinsSegment(JenkinsSegment):
    ok_icon = u'\uF118'
    fail_icon = u'\uF119'
    FAILED_TEST_MARKER = 'F'
    ERROR_TEST_MARKER = 'E'

    def __init__(self, *args, **kwargs):
        self.blink_state = 0
        self.verbose_name = kwargs.pop('verbose_name', kwargs['job_name'])

        super(PyTestJenkinsSegment, self).__init__(*args, **kwargs)

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

    def _get_build_status(self, build):
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

ft = PyTestJenkinsSegment(job_name='aginoodle_FT', verbose_name='FT')
mt = PyTestJenkinsSegment(job_name='aginoodle_MT', verbose_name='MT')
ut = PyTestJenkinsSegment(job_name='aginoodle_UT', verbose_name='UT')
pylint = PylintJenkinsSegment(job_name='aginoodle_pylint')
