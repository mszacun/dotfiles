from __future__ import (unicode_literals, division, absolute_import, print_function)
from powerline.lib.threaded import ThreadedSegment
import urllib2
import re
from jenkinsapi.jenkins import Jenkins


class JenkinsJobStatus(object):
    blink = False


class JenkinsRunningJobStatus(JenkinsJobStatus):
    blink = True


class JenkinsGoingToFailJobStatus(JenkinsRunningJobStatus):
    good = False


class JenkinsSoFarOKStatus(JenkinsRunningJobStatus):
    good = True


class JenkinsFailedStatus(JenkinsJobStatus):
    good = False


class JenkinsPassedStatus(JenkinsJobStatus):
    good = True

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
                return JenkinsSoFarOKStatus()

            test_results_text = console_text[test_results_start_index:]

            if  (test_results_text.find(self.FAILED_TEST_MARKER) != -1 or
                 test_results_text.find(self.ERROR_TEST_MARKER) != -1):
                return JenkinsGoingToFailJobStatus()
            else:
                return JenkinsSoFarOKStatus()

        def get_build_status(self, job_name):
            jenkins = Jenkins(self.JENKINS_URL)

            job = jenkins.get_job(job_name)
            build = job.get_last_build()

            if build.is_running():
                return self.get_running_build_status(build)
            else:
                return JenkinsPassedStatus() if build.is_good() else JenkinsFailedStatus()

	def update(self, old_value):
            return self.get_build_status(self.job_name)

	def render(self, job_status, **kwargs):
            highlight_groups = []

            self.blink_state = (self.blink_state + 1) % 2
            icon = self.ok_icon if job_status.good else self.fail_icon
            if job_status.blink:
                highlight_groups.append('working_' + ('ok' if job_status.good else 'fail'))

            content = ' ' if self.blink_state and job_status.blink else icon
            content += ' ' + self.verbose_name

            result = {'contents': content}
            if highlight_groups:
                result['highlight_groups'] = highlight_groups

            return [result]

ft = JenkinsSegment(job_name='aginoodle_FT', verbose_name='FT')
mt = JenkinsSegment(job_name='aginoodle_MT', verbose_name='MT')
ut = JenkinsSegment(job_name='aginoodle_UT', verbose_name='UT')
