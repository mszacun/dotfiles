from datetime import datetime, timedelta
from dateutil import parser
import subprocess
import json


class TimewarriorEntry:
    def __init__(self, raw_entry):
        self.id = raw_entry['id']
        self.start = parser.isoparse(raw_entry['start'])
        self.end = parser.isoparse(raw_entry['end'])
        self.tag = raw_entry['tags'][0]

    def __str__(self):
        return str(self.start)


output = [TimewarriorEntry(e) for e in json.loads(subprocess.check_output(['timew', 'export', 'today']).decode())]
for i in output:
    print(i)
