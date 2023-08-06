# source: http://code.activestate.com/recipes/413393-multiple-reader-one-writer-mrow-resource-locking/
import threading
from threading import get_ident


def acquireLocked(fn):
    def _acquireLocked_wrapper(self, *args, **kw):
        L = self.acquireLock
        try:
            L.acquire()
            result = fn(self, *args, **kw)
        finally:
            L.release()
        return result

    return _acquireLocked_wrapper


def releaseLocked(fn):
    def _releaseLocked_wrapper(self, *args, **kw):
        L = self.releaseLock
        try:
            L.acquire()
            result = fn(self, *args, **kw)
        finally:
            L.release()
        return result

    return _releaseLocked_wrapper


class RWLock(object):
    """MROW resource lock."""

    def __init__(self):
        self.acquireLock = threading.Lock()
        self.releaseLock = threading.Lock()
        self.sublocks = []
        self.waiting = []
        self.readers = 0
        self.writing = False
        self.threadReaders = {}
        self.threadWriters = {}

    def get_lock(self, type='reader'):
        if type == 'writer':
            return self.writer()
        else:
            return self.reader()

    def reader(self):
        """Return an acquired read lock."""
        threadReaders, threadWriters = self.threadReaders, self.threadWriters
        ident = get_ident()
        if ident in threadReaders:
            sublock, count = threadReaders[ident]
            threadReaders[ident] = (sublock, count + 1)
            return sublock
        elif ident in threadWriters:
            # Writers are inherently readers, so treat as a reentrant
            # write lock.
            sublock, count = threadWriters[ident]
            threadWriters[ident] = (sublock, count + 1)
            return sublock
        sublock = RLock(self)
        if self.writing:
            # Wait for acquired writers to release.
            self.waiting.append(sublock)
            sublock.acquire()
        sublock.acquire()
        self.readers += 1
        self.sublocks.append(sublock)
        threadReaders[ident] = (sublock, 1)
        return sublock

    reader = acquireLocked(reader)

    def writer(self):
        """Return an acquired write lock."""
        threadReaders, threadWriters = self.threadReaders, self.threadWriters
        ident = get_ident()
        wasReader = False
        if ident in threadWriters:
            sublock, count = threadWriters[ident]
            threadWriters[ident] = (sublock, count + 1)
            return sublock
        elif ident in threadReaders:
            # Readers-turned-writers must wait for any reads to complete
            # before turning into writers.
            sublock, count = threadReaders[ident]
            del threadReaders[ident]
            self.readers -= 1
            self.sublocks.remove(sublock)
            wasReader = True
        sublock = WLock(self)
        if self.readers or self.writing:
            # Wait for acquired readers/writers to release.
            self.waiting.append(sublock)
            sublock.acquire()
        sublock.acquire()
        self.writing = True
        self.sublocks.append(sublock)
        if not wasReader:
            count = 0
        threadWriters[ident] = (sublock, count + 1)
        return sublock

    writer = acquireLocked(writer)

    def _releaseR(self, sublock):
        sublocks = self.sublocks
        if sublock in sublocks:
            threadReaders = self.threadReaders
            ident = get_ident()
            count = threadReaders[ident][1] - 1
            if count:
                threadReaders[ident] = (sublock, count)
            else:
                del threadReaders[ident]
                self.readers -= 1
                sublocks.remove(sublock)
                waiting = self.waiting
                if waiting and not self.readers:
                    # If a lock is waiting at this point, it is a write lock.
                    waiting.pop(0)._release()

    _releaseR = releaseLocked(_releaseR)

    def _releaseW(self, sublock):
        sublocks = self.sublocks
        if sublock in sublocks:
            threadWriters = self.threadWriters
            ident = get_ident()
            count = threadWriters[ident][1] - 1
            if count:
                threadWriters[ident] = (sublock, count)
            else:
                del threadWriters[ident]
                self.writing = False
                sublocks.remove(sublock)
                waiting = self.waiting
                # Release any waiting read locks.
                while waiting and isinstance(waiting[0], RLock):
                    waiting.pop(0)._release()

    _releaseW = releaseLocked(_releaseW)


class SubLock(object):

    def __init__(self, rwlock):
        self.lock = threading.Lock()
        self.rwlock = rwlock

    def _release(self):
        self.lock.release()

    def acquire(self):
        self.lock.acquire()


class RLock(SubLock):

    def release(self):
        self.rwlock._releaseR(self)


class WLock(SubLock):

    def release(self):
        self.rwlock._releaseW(self)
