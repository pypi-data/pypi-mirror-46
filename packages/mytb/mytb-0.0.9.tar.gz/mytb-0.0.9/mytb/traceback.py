from __future__ import absolute_import
from __future__ import print_function

import traceback

def print_stack():
    traceback.print_stack(limit=-5)
