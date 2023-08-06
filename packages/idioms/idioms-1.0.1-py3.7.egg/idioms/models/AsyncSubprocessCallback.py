import subprocess
import json
class AsyncSubprocessCallback:
    @property
    def _arity(self):
        return self.callback.func_code.co_argcount - 1
    def __call__(self, stdout=None, stderr=None, process=None):
        reason = None
        out = None
        err = None
        if not isinstance(stdout, bytes):
            reason = f"Expected bytes in position 1, got: {type(stdout)}"
        if not isinstance(stderr, bytes):
            reason = f"Expected bytes in position 2, got: {type(stderr)}"
        if not isinstance(process, subprocess.Popen):
            reason = f"Expected subprocess.Popen in position 3, got: {type(process)}"
        if reason:
            args = locals()
            err = TypeError(f"Could not execute AsyncSubprocessCallback: {reason} {args}")
        else:
            try:
                out = self.callback(stdout, stderr, process)
                self.executed = True
            except Exception as e:
                err = e
        self.args = json.dumps({"stdout": stdout, "stderr": stderr, "process": process}, default=lambda x: str(x))
        self.ok = err is None
        self.out = out
        self.err = err
        return self
    def __str__(self):
        return str(self.out)
    def __repr__(self):
        return json.dumps({'ok': self.ok, 'executed': self.executed, 'args': self.args, 'out': self.out, 'err': self.err, 'callback': self.callback}, default=lambda x: str(x))
    def __init__(self, callback):
        self.callback = callback
        self.ok = None
        self.out = None
        self.err = None


