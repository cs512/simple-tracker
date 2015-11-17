#!/usr/bin/env python
# coding=utf-8

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class simplewatchdog():

    def __init__(self, folderpath):
        self.folderpath = folderpath

    def start(self): 
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        event_handler = LoggingEventHandler()
        self.observer = Observer()
        self.observer.schedule(event_handler, self.folderpath, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def end(self):
        self.observer.stop()
