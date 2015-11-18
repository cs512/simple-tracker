#!/usr/bin/env python
# coding=utf-8
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

need_update = False


class SimpleEventHandler(LoggingEventHandler):
    """Logs all the events captured."""

    def on_moved(self, event):
        global need_update
        need_update = True

    def on_created(self, event):
        global need_update
        need_update = True

    def on_deleted(self, event):
        global need_update
        need_update = True

    def on_modified(self, event):
        global need_update
        need_update = True


class SimpleWatchDog:

    def __init__(self, folderpath, STClientInstance, local_ip):
        self.folderpath = folderpath
        self.observer = Observer()
        self.stc = STClientInstance
        self.local_ip = local_ip

    def start(self):
        global need_update
        event_handler = SimpleEventHandler()
        self.observer.schedule(event_handler, self.folderpath, recursive=True)
        self.observer.start()

        while True:
            time.sleep(10)
            #print(need_update)
            if need_update:
                print("the folder needs update")
                self.stc.update(self.local_ip)
                need_update = False
                print("the folder had updated")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def end(self):
        self.observer.stop()
