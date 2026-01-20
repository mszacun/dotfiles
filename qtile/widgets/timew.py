import subprocess
from datetime import datetime, timedelta

from libqtile.widget import base
from libqtile.log_utils import logger


class Timew(base.BackgroundPoll):
    update_interval = 1.0
    notification_interval = timedelta(minutes=10)

    def __init__(self, **config):
        super().__init__('', **config)

        self.last_notification = datetime.now()

    def poll(self):
        try:
            output = subprocess.check_output('timew').decode().splitlines()
            if len(output) > 2:
                task_name = output[0][len('Tracking'):].strip().strip('"')
                total_time = output[3][len('  Total'):].strip()
                self.running = True
                return f'{task_name} - {total_time}'
        except subprocess.CalledProcessError as e:
            self.running = False
            self._display_no_time_tracking_notification()
            return ''

    def _display_no_time_tracking_notification(self):
        current_time = datetime.now()
        if self._is_working_day(current_time) and self._is_working_hours(current_time) and self._enough_time_since_last_notification(current_time):
            subprocess.run(['notify-send', '-u', 'CRITICAL', 'Timew', 'No time tracking in progress'])
            self.last_notification = datetime.now()

    def _is_working_day(self, t):
        return t.weekday() not in [5, 6]

    def _is_working_hours(self, t):
        return 8 < t.hour < 18

    def _enough_time_since_last_notification(self, t):
        return (t - self.last_notification) >= self.notification_interval
