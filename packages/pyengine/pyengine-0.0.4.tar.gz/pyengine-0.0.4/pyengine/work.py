# encoding=utf-8
from multiprocessing import Process
from threading import Thread
import platform
import sys
import os

is_win = False
if platform.platform().upper().find('WIN') != -1:
    is_win = True

if not is_win:
    import signal
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
is_py2 = False
if sys.version[0] == '2':
    is_py2 = True


def async_work_res(_res_deal):
    def wrapper(func):
        def inner(*args, **kwargs):
            if is_win:
                My_Job_With_Thread(_res_deal=_res_deal, target=func, args=args, kwargs=kwargs).start()
            else:
                My_Job_With_Process(_res_deal=_res_deal, target=func, args=args, kwargs=kwargs).start()
            return 'ok'
        return inner
    return wrapper


class My_Job_With_Thread(Thread):

    def __init__(self, _res_deal, *args, **kwargs):
        self._res_deal = _res_deal
        Thread.__init__(self, *args, **kwargs)

    def run(self):
        try:
            if is_py2:
                self._res_deal(self._Thread__target(*self._Thread__args, **self._Thread__kwargs))
            else:
                self._res_deal(self._target(*self._args, **self._kwargs))
        except Exception as e:
            raise e
        finally:
            if is_py2:
                del self._Thread__target;
                del self._Thread__args;
                del self._Thread__kwargs
            else:
                del self._target, self._args, self._kwargs


class My_Job_With_Process(Process):
    def __init__(self, _res_deal, *args, **kwargs):
        self._res_deal = _res_deal
        Process.__init__(self, *args, **kwargs)

    def run(self):
        if self._target:
            self._res_deal(self._target(*self._args, **self._kwargs))


def async_work():
    def wrapper(func):
        def inner(*args, **kwargs):
            if is_win:
                Job_With_Thread(target=func, args=args, kwargs=kwargs).start()
            else:
                Job_With_Process(target=func, args=args, kwargs=kwargs).start()
            return 'ok'
        return inner
    return wrapper


class Job_With_Thread(Thread):

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)

    def run(self):
        try:
            if is_py2:
                self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            else:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            raise e
        finally:
            if is_py2:
                del self._Thread__target;
                del self._Thread__args;
                del self._Thread__kwargs
            else:
                del self._target, self._args, self._kwargs


class Job_With_Process(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            raise e
        finally:
            os._exit(0)


    def start(self):
        pid = os.fork()
        if pid == 0:
            pass
        else:
            return pid


