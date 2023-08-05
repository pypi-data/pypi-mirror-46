#!python

import argparse
import os
import time

from subprocess import Popen

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class TestRunnerEventHandler(LoggingEventHandler):

    def __init__(self, *args, **kwargs):
        file_name = kwargs.pop('file')

        super(TestRunnerEventHandler, self).__init__(*args, **kwargs)

        self.successful = False
        self.file = open(file_name, 'a')
        self.program = file_name

    def on_any_event(self, event):
        if event.is_directory:
            return

        ignore_list = ['.git/']
        for extension in ignore_list:
            if extension in event.src_path:
                return

        print('File changed: {}'.format(event.src_path))

        process = Popen(['python', self.program], shell=False)
        process.wait()

        if process.returncode == 0:
            self.successful = True
        else:
            self.successful = False

        self.write_to_target(self.successful)

    def write_to_target(self, status):
        pass


def main_loop():

    parser = argparse.ArgumentParser(description=('Python Dojo checks file for test.'))
    parser.add_argument('file', help='The python test file to be watched.', default='.')
    parser.add_argument('--target', help='The device target.', default='.')

    args = parser.parse_args()

    print('Starting to watch file', args.file)

    local_path = os.getcwd()

    observer = Observer()
    handler = TestRunnerEventHandler(file=args.file)
    observer.schedule(handler, local_path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
        handler.file.close()

    observer.join()
