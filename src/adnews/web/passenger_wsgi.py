import sys
import os

INTERP = "/var/www/u3198937/data/flaskenv/bin/python"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

from app import application
