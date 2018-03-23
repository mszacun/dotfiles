from datetime import datetime, timedelta
import os
import re

from libqtile.widget import base

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
            progress = str(int(100 * self.completed_tests_number / float(self.all_tests_number)))
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


class JenkinsWidget(base.ThreadedPollText):
    JENKINS_URL = 'http://wrling17.emea.nsn-net.net:9090/'

    jenkins_status_update_interval = timedelta(seconds=15)
    update_interval = 1 # To toggle blinking state

    def __init__(self, *args, **kwargs):
        base.ThreadedPollText.__init__(self, *args, **kwargs)

        self.blink_state = 0
        self.last_jenkins_status_update = datetime(1993, 6, 13)
        self.job_status = None

    def _configure(self, qtile, bar):
        super(JenkinsWidget, self)._configure(qtile, bar)
        self.layout = self.drawer.textlayout(
            self.text,
            self.foreground,
            self.font,
            self.fontsize,
            self.fontshadow,
            markup=True
        )

    def tick(self):
        self.blink_state = (self.blink_state + 1) % 2

        if datetime.now() - self.last_jenkins_status_update > self.jenkins_status_update_interval:
            self.last_jenkins_status_update = datetime.now()
            super(JenkinsWidget, self).tick()
        else:
            self.update(self.render(self.job_status))

    def poll(self):
        build = self._get_last_build(self.job_name)
        new_value = self._get_build_status(build)

        if type(new_value) != type(self.job_status):
            new_value.show_notification(self.job_name)

        self.job_status = new_value
        return self.render(self.job_status)

    def _get_last_build(self, job_name):
        jenkins = Jenkins(self.JENKINS_URL)

        job = jenkins.get_job(job_name)
        return job.get_last_build()

    def button_press(self, x, y, button):
        last_build = self._get_last_build(self.job_name)

        if last_build.is_running():
            last_build.stop()
        else:
            jenkins = Jenkins(self.JENKINS_URL)
            job = jenkins.get_job(self.job_name)
            job.invoke()



class PyTestJenkinsWidget(JenkinsWidget):
    ok_icon = u'\uF00C'
    fail_icon = u'\uF00D'
    FAILED_TEST_MARKER = 'F'
    ERROR_TEST_MARKER = 'E'
    COLOR_FAIL = 'AB4642'
    COLOR_OK = 'A1B56C'

    def __init__(self, *args, **kwargs):
        JenkinsWidget.__init__(self, *args, **kwargs)

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
        if job_status:
            icon = self.ok_icon if job_status.good else self.fail_icon
            self.foreground = self.COLOR_OK if job_status.good else self.COLOR_FAIL

            icon = ' ' if self.blink_state and job_status.running else icon
            progress = job_status.get_progress()

            if progress:
                return '{} {} <b>{}</b>'.format(progress, self.verbose_name, icon)
            else:
                return '{} <b>{}</b>'.format(self.verbose_name, icon)


class CookerJenkinsWidget(JenkinsWidget):
    ok_icon = u'\uF00C'
    fail_icon = u'\uF00D'
    COLOR_FAIL = 'AB4642'
    COLOR_OK = 'A1B56C'

    def __init__(self, *args, **kwargs):
        JenkinsWidget.__init__(self, *args, **kwargs)

    def _get_build_status(self, build):
        if build.is_running():
            return self.get_running_build_status(build)
        else:
            return JenkinsPassedStatus() if build.is_good() else JenkinsFailedStatus()

    def get_running_build_status(self, build):
        console_text = build.get_console().split('\n')
        all_tests_number = self._get_number_of_all_tests(console_text)
        completed_tests_number = self._get_number_of_completed_tests(console_text)

        if any((line.startswith('failed') for line in console_text)):
            return JenkinsGoingToFailJobStatus(completed_tests_number, all_tests_number)
        else:
            return JenkinsSoFarOKStatus(completed_tests_number, all_tests_number)

    def _get_number_of_all_tests(self, console_text):
        regexp = re.compile(r'Prepared (\d+) tests')

        for line in console_text:
            match = regexp.search(line)
            if match:
                return match.group(1)

    def _get_number_of_completed_tests(self, console_text):
        return len([line for line in console_text if self._is_completed_test_line(line)])

    def _is_completed_test_line(self, line):
        completed_test_suffixes = {'success', 'failed', 'error'}
        return any(line.startswith(suffix) for suffix in completed_test_suffixes)

    def render(self, job_status, **kwargs):
        if job_status:
            icon = self.ok_icon if job_status.good else self.fail_icon
            self.foreground = self.COLOR_OK if job_status.good else self.COLOR_FAIL

            icon = ' ' if self.blink_state and job_status.running else icon
            progress = job_status.get_progress()

            if progress:
                return '{} {} <b>{}</b>'.format(progress, self.verbose_name, icon)
            else:
                return '{} <b>{}</b>'.format(self.verbose_name, icon)
