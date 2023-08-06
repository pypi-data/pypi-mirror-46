import os
from idioms.models.AsyncSubprocess import AsyncSubprocess
from idioms.utils.soundutils import play as play_sound
from termcolor import colored
class SoundFx:
    def __init__(self, master_volume, suppress_log_messages=False, loglevel='WARNING', *load_dirs):
        self.sounds = {}
        self.loglevel = loglevel
        self.suppress_log_messages = suppress_log_messages
        self.volume = master_volume
        try:
            soundfx_dir = os.environ['SOUNDFX_PATH']
        except:
            soundfx_dir = None
        self.source_dirs = [soundfx_dir] + list(load_dirs)
        for directory in self.source_dirs:
            count = 0
            if soundfx_dir and os.path.isdir(directory):
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    self.sounds[filename] = filepath
                    count += 1
            print(colored(f"Loaded {count} files from directory {directory}", 'green'))
    def shuffle(self):
        i = 0
        colors = ['red', 'yellow', 'green', 'blue', 'magenta', 'cyan', 'white']
        for k,v in self.sounds.items():
            color = colors[i%len(colors)]
            info = AsyncSubprocess(cmd=f'soxi {k}', silent=True, autostart=True)
            msg = colored(f"{i}. {k}", color, attrs=['bold'])
            player = AsyncSubprocess(cmd=f'play --volume {self.volume} {v}', timed=True, autostart=False, loglevel='WARNING', silent=False)
            print(msg)
            info.read()
            output = info.output.replace("\n", "\n        ")
            print(output)
            player.run()
            i += 1
    def play(self, sound, volume_coefficient=None, suppress_log_output=False):
        if volume_coefficient is None:
            volume_coefficient = self.volume
        if os.path.isfile(sound):
            filepath = sound
        elif sound in self.sounds:
            filepath = self.sounds[sound]
        else:
            raise ValueError(f"No match found for sound: '{sound}'")
        play_sound(filepath, volume_coefficient, autostart=True,loglevel=self.loglevel,suppress_log_messages=self.suppress_log_messages)

        



