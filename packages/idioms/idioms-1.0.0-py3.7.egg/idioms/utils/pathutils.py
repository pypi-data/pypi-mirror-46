import os

def realpath(filepath):
    """Return the real path corresponding to the given filepath, expanding any tildes and resolving symlinks."""
    return os.path.realpath(os.path.abspath(os.path.expanduser(filepath)))