import sys
import time
from threading import Thread

import logging


class Spinner:
    """
        A python class to provide simple loading feature, thread based to a python application
    """

    # character interval changing time
    SLOW = 0.2
    NORMAL = 0.15
    FAST = 0.05

    def __init__(self, change_interval=NORMAL):
        """Set the load proprity to True"""
        self.load = True
        self.change_interval = change_interval

    def _spinning_cursor(self):
        """ A generator which itterate over the string element and yield it"""
        while True:
            for cursor in '|/-\\':
                yield cursor

    def _thread_spin(self):
        """ Handle the display of the different yielded elements"""
        spinner = self._spinning_cursor()

        try:
            while self.load:
                sys.stdout.write(next(spinner))
                sys.stdout.flush()
                time.sleep(self.change_interval)  # time to wait before changing the element
                sys.stdout.write('\b')

        except KeyboardInterrupt:
            pass

    def spin(self):
        t = Thread(target=self._thread_spin)
        t.start()
        # t.join()

    def stop(self):
        self.load = False

# spinner = Spinner();

# spinner.spin()

# time.sleep(50)

# spinner.stop()
