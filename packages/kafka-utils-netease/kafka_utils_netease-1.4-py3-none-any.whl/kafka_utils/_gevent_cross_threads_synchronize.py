__all__ = ['Lck', 'Cond', 'Evnt']


import gevent
from gevent import monkey
Lck = monkey.get_original('threading', 'Lock')


class Cond:
    def __init__(self, lock):
        self._lock = lock
        self._waiters = []

    def _is_locked(self):
        return not self._lock.acquire(blocking=False)

    def wait(self, timeout=None):
        if not self._is_locked():
            raise RuntimeError("cannot wait on un-acquired lock")
        hub = gevent.get_hub()
        loop = hub.loop
        asyn = loop.async_()
        self._waiters.append(asyn)
        self._lock.release()
        with gevent.Timeout(timeout, False):
            hub.wait(asyn)
        self._lock.acquire()

    def notify(self):
        if not self._is_locked():
            raise RuntimeError("cannot notify on un-acquired lock")
        if not self._waiters:
            return
        asyn = self._waiters.pop(0)
        asyn.send()

    def notify_all(self):
        if not self._is_locked():
            raise RuntimeError("cannot notify on un-acquired lock")
        for asyn in self._waiters:
            asyn.send()

    def __enter__(self):
        self._lock.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.__exit__(exc_type, exc_val, exc_tb)


class Evnt:
    def __init__(self):
        self._lock = Lck()
        self._cond = Cond(self._lock)
        self._counter = 0

    def wait(self, timeout=None):
        with self._cond:
            with gevent.Timeout(timeout, False):
                while self._counter <= 0:
                    self._cond.wait(timeout)
            if self._counter > 0:
                self._counter -= 1

    def set(self):
        with self._cond:
            self._counter += 1
            self._cond.notify()

    def clear(self):
        with self._cond:
            self._counter = 0

    def __enter__(self):
        self._cond.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cond.__exit__(exc_type, exc_val, exc_tb)
