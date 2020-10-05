import subprocess

from libqtile.widget import base
from libqtile.log_utils import logger


class Timew(base.ThreadedPollText):
    update_interval = 1.0

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
            return ''

    def button_press(self, x, y, button):
        if self.running:
            subprocess.run(['timew', 'stop'])
