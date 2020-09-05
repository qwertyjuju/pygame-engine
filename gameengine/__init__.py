"""Importing all game engine modules"""
import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)

from main import *
from _gameobject import *
from _managers import *
from _scene import *