#!/usr/bin/env python3


import subprocess
import sys

class InContenerCommandRunner:
    def __init__(self, input_file, command):
        self.input_file = input_file
        self.command = command

    def run_pylint(self, post_process_func=None):
        command = self.command + [self.input_file]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            output_lines = result.stdout.splitlines()
            self._process_output_lines(output_lines, post_process_func)
        except subprocess.CalledProcessError as e:
            output_lines = e.stdout.splitlines()
            self._process_output_lines(output_lines, post_process_func)
            self._print_error_message(e.stderr)

    def _process_output_lines(self, output_lines, post_process_func=None):
        for line in output_lines:
            processed_line = line if post_process_func is None else post_process_func(line)
            print(processed_line)

    def _print_error_message(self, error_message):
        error_message = error_message.strip()
        if error_message:
            print(f"Error: {error_message}")

# Example post-processing function: Strip prefix from each line
def strip_prefix(line):
    if line.startswith('identt2check'):
        line = 'web/' + line
    return line

# Usage example
input_file = sys.argv[1].replace('web/', '')
command = [
    'docker',
    'compose',
    'exec',
    'web',
    'pylint',
    '--output-format=text',
    '--msg-template="{path}:{line}:{column}:{C}: [{symbol}] {msg} [{msg_id}]"',
    '--reports=no',
]
pylint_runner = InContenerCommandRunner(input_file, command=command)
pylint_runner.run_pylint(post_process_func=strip_prefix)
