from __future__ import division
import sys
from math import ceil


class ProgressBar():
    def __init__(self, label="Running:", bar_length=10, full_marker = u"\u25FC ", empty_marker = u"\u25FB "):
        self.label = label
        self.bar_length = bar_length
        self.full_marker = full_marker
        self.empty_marker = empty_marker

    def progress(self, current=5, total=100):
        full_blocks = int(ceil(current / total * self.bar_length))
        empty_blocks = int(self.bar_length - full_blocks)
        print(self.label + self.full_marker  * full_blocks + self.empty_marker * empty_blocks)
        sys.stdout.write("\033[F")
