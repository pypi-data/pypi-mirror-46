from idioms.models.AsyncSubprocess import AsyncSubprocess
import sys
import os

def play(path_to_soundfile, volume_coeff=1, autostart=True, loglevel='ERROR', suppress_log_messages=True):
    """Plays a sound file at the provided filepath.

    Args:
          volume_coeff: scales the amplitude by the given coefficient. 1=unchanged, 0=mute. Max value = 1.5
          autostart: if True, play sound immediately; otherwise, thread will be initialized and returned, but caller must manually invoke the start() method of the returned thread object. (Default: True)
          loglevel: minimum log priority level to print to console
          suppress_log_messages: whether to suppress log output of AsyncSubprocess"""

    if not os.path.isfile(path_to_soundfile):
        raise FileNotFoundError(f"Couldn't find a sound file to play at the requested filepath: {path_to_filepath}")

    if volume_coeff > 1.5:
        raise ValueError(f"volume_coeff too high. Maximum permitted value for this multiplier is 1.5")

    cmd = f"play --volume {volume_coeff} {path_to_soundfile} --multi-threaded"
    p = AsyncSubprocess(cmd=cmd, loglevel=loglevel, silent=suppress_log_messages, autostart=autostart)
    return p
