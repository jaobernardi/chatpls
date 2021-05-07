import signal
import sys
from .methods import processes
import os
import logging


signal.signal(signal.SIGINT, (lambda sig, frame: sys.exit()))
