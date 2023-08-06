from collections import OrderedDict
import signal
import subprocess
import time
import shlex
import datetime
from bitstring import BitArray
import logging
import json
from copy import copy
from gemeinsprache.utils import Pretty as pp
from math import inf as Infinity
import sys
sys.path.insert(0, '/home/kz/projects/idioms/models')
from .AsyncSubprocessCallback import AsyncSubprocessCallback
import os
# symbols
WAITING = 'WAITING'
RUNNING = 'RUNNING'
COMPLETE = 'COMPLETE'
OK = 'OK'
ERROR = 'ERROR'
ABORTED = 'ABORTED'
import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-9s) %(message)s',
)


class AsyncSubprocess(threading.Thread):
    @property
    def possible_states(self):
        return ABORTED, ERROR, OK, RUNNING, WAITING

    def __str__(self):
        d = self.to_dict()
        try:
            d['_pipes'][0] = d['_pipes'][0].decode("utf-8")
            d['_pipes'][1] = d['_pipes'][1].decode("utf-8")
        except:
            pass
        return json.dumps(d, indent=4, sort_keys=True, default=lambda x: str(x))

    @property
    def _default_args(self):
        return {'autostart': True, 'callback': None, 'timeout': None, 'poll_interval': 0.001, 'timed': False, "_path_to_pwd": "/home/kz/.ptpython/.pwd", "_pwd_env_var": "PTPYTHON_PWD"}

    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 loglevel="ERROR", silent=False, **kwargs):
        super(AsyncSubprocess, self).__init__(group=None,
                                              target=None,
                                              name=None)
        self.args = args
        self.kwargs = kwargs
        self.logger = logging.getLogger(__name__)
        self.loglevel = loglevel
        self.logger.setLevel(self.loglevel)
        self._pipes = None
        self._processed = None
        self._pwd_env_var = None
        self._aborted = False
        self._callback_fired = False
        self._callback_complete = False
        self._path_to_pwd = None
        self.cmd = None
        self.autostart = None
        self.poll_interval = None
        self.timed = None
        self.callback = None
        self.timeout = Infinity
        self.silent = silent
        self.process = None
        self.time_started = None
        self.time_completed = None
        self.start()
        return
    
    def log(self, level, msg):
        if not self.silent:
            f = getattr(self.logger, level)
            f(msg)

    def start(self):
        locals().update(self._default_args)
        locals().update(self.kwargs)
        for k,v in locals().items():
            setattr(self, k, v)
        self.process = None
        self.log('info',
            f"Initialized new AsyncSubprocess thread with cmd: '{self.cmd}'")
        if self.has_callback:
            self.callback = AsyncSubprocessCallback(self.callback)
        if self.autostart:
            self.run()
        return
    
    @property
    def pwd(self):
        with open(self._path_to_pwd, 'r') as f:
            return  f.read().strip()
    @property
    def pwd_dict(self):
        return {self._pwd_env_var: self.pwd}
    
    def set_pwd(self, new_path):
        with open(self._path_to_pwd, 'w') as f:
            f.write(new_path)
        return {self._pwd_env_var: new_path}

    def run(self):
        self.log('info', f"Running thread {self.name}")
        self.time_started = datetime.datetime.now()
        cmd = "cd \"$(" + self._pwd_env_var + ")\" && " + self.cmd + " && echo \"\n$(pwd)\""
        self.process = subprocess.Popen(cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        env=self.pwd_dict)
        if self._is_event_loop:
            duration = self.poll_interval
            max_wait = datetime.timedelta(seconds=self.timeout) if self.has_timeout else 9999999999
            has_timeout = self.has_timeout
            keep_going = self.is_running
            while keep_going:
                if has_timeout and datetime.datetime.now() - self.time_started > max_wait:
                    self._aborted = True
                    self.kill()
                    self.log('warning', f"Process aborted after {self.timeout} seconds due to timeout")
                    break
                keep_going = self.is_running
                time.sleep(duration)
            self.time_completed = datetime.datetime.now()
            if not self._aborted:
                try:
                    self._pipes = self.process.communicate()


                except Exception as e:
                    self.log('warning', f"Error communicating with self.process: {e}. Unsetting self._pipes to None (was {self._pipes})")
                    self._pipes = None
                self.log("error", f"My pwd is: {self.pwd}")
                if self.ok and self.has_callback:
                    args = list(self._pipes) + [self.process]
                    try:
                        self._callback_fired = True
                        self._processed = self.callback(*args)
                    except Exception as e:
                        self.log('error', f"Error executing callback with args {args}: {e}")
                    self._callback_complete = True

        return

    def __iter__(self):
        for k, v in self.to_dict().items():
            yield k, v

    @property
    def pid(self):
        _pid = None
        try:
            _pid = self.process.pid
        except:
            pass
        return _pid

    @property
    def pgid(self):
        _pgid = None
        try:
            _pgid = os.getpgid(self.pid)
        except:
            pass
        return _pgid

    def kill(self):
        self.log('warning', f"Killing process {self.pid}")
        try:
            os.kill(self.pid, signal.SIGINT)
        except Exception as e:
            self.log('error', f"Failed to kill process {self.pid}: {e}")



    def killpg(self):
        self.log('warning', f"Killing process group {self.pgid}...")
        try:
            os.killpg(self.pgid, signal.SIGINT)
        except Exception as e:
            self.log('error', f"Failed to kill process group {self.pgid}: {e}")

    @property
    def _state(self) -> int:
        return [self._aborted, self.has_error, self.ok, self.is_complete, self.is_initialized].index(True)

    @property
    def _is_event_loop(self) -> int:
        return int(bool(self.has_callback or self.has_timeout or self.timed))

    @property
    def has_timeout(self) -> bool:
        return bool(self.timeout and Infinity > self.timeout > 0)

    @property
    def has_callback(self) -> bool:
        return bool(self.callback and self.callback is not None)

    @property
    def is_initialized(self) -> bool:
        return bool(self.process)

    @property
    def is_running(self) -> bool:
        return bool(self._aborted is False and self.is_initialized and self.process and self.process.poll(
        ) is None)

    @property
    def is_complete(self) -> bool:
        return bool(self.is_initialized and not self.is_running)

    @property
    def ok(self) -> bool:
        return bool(self.is_complete and not self.exitcode and not self._aborted and self._pipes)

    @property
    def has_error(self) -> bool:
        return bool(self.is_complete and self.exitcode)

    @property
    def status(self):
        return self.possible_states[self._state]

    @property
    def exec_time(self):
        # if not self._is_event_loop:
        #     self.logger.error(f"Process not an event loop! Run with args \"{'timed': True}\" to collect timing information.")
        #     return
        try:
            _dt = self.time_completed - self.time_started
            return (float(f"{_dt.seconds}.{str(_dt.microseconds).zfill(6)}"), "seconds")
        except Exception as e:
           # self.logger.error(f"Execution time could not be calculated: {e}")
           dt = "Not captured"
        return dt

    def read(self):
        out = b""
        if self._pipes:
            return self._pipes[0]
        try:
            i = 0
            duration = self.poll_interval
            while self.is_running:
                if i % 10000 == 0:
                    self.log('info',
                        f"Waiting for thread {self.name} to finish running...")
                i += 1
                time.sleep(duration)
            self._pipes = self.process.communicate()
            out = self._pipes[0]
            lines = self._pipes[0].split(b"\n")
            self._pipes[0] = 'b\n'.join(lines[:-2])
            pwd = lines[-2].decode("utf-8")
            self.set_pwd(pwd)
        except AttributeError:
            pass

        return self._pipes[0]

    @property
    def stdout(self):
        if self.is_complete and not self._aborted:
            self.read()
        try:
            return self._pipes[0]
        except:
            return b''

    @property
    def output(self):
        raw = self.stdout
        out = self._processed if self.has_callback is True else raw.decode("utf-8")
        return out

    @property
    def stderr(self):
        if self.is_complete and not self._aborted:
            self.read()
        try:
            return self._pipes[1]
        except:
            return b''

    @property
    def error(self):
        err = self.stderr.decode("utf-8")
        return err

    @property
    def exitcode(self):
        try:
            return self.process.returncode
        except AttributeError:
            return -1

    def to_dict(self):
        if self.is_complete and not self._aborted:
            self.read()
        unserializable_attrs = ['_stderr', '_started', 'logger', 'process', 'self']
        computed_attrs = ['_state', 'output', 'error', 'is_initialized', 'is_running', 'is_complete', 'ok', '_aborted', '_path_to_pwd', 'pwd',
                          'has_error', 'has_callback', '_callback_fired', '_callback_complete', '_processed', 'status', 'exitcode', 'possible_states', 'exec_time']
        d = copy(self.__dict__)
        d['time_started'] = d['time_started'].isoformat()
        try:
            d['time_completed'] = d['time_completed'].isoformat()
        except AttributeError:
            d['time_completed'] = None

        for attr in unserializable_attrs:
            del d[attr]
        for attr in computed_attrs:
            v = getattr(self, attr)
            if isinstance(v, bytes):
                v = v.decode("utf-8")
            d[attr] = v
        return OrderedDict(sorted(d.items()))

    def to_json(self):
        if self.is_complete and not self._aborted:
            self.read()
        return self.__str__()

    def print(self, pretty=True):
        s = self.to_dict()
        if pretty:
            s = pp(s)
        print(s)


