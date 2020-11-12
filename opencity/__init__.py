import os

version_path = os.path.join(os.path.dirname(__file__),"VERSION")

with open(version_path) as f:
    line = f.readline()
    __version__ = line