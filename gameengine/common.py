import os, sys

from _managers import *

try:
    import settings
except ImportError:
    print('settings file not found')

try:
    import loadinglist
except ImportError:
    print('loading file not found')
        
        
def initialize():
    global TITLE, SCREENWIDTH, SCREENHEIGHT, LOADERDICT, DATADICT, EVENTDICT, BLITLIST, GAMERUNNING, CURRENTFPS, MANAGERS
    TITLE = settings.__title__
    SCREENWIDTH = settings.screen_width
    SCREENHEIGHT = settings.screen_height
    LOADERDICT = {
        '_loadlist':[],
        '_unloadlist':[],
    }
    DATADICT = {}
    EVENTDICT = {}
    BLITLIST = []
    GAMERUNNING = True
    CURRENTFPS = 0
    MANAGERS = [
        DataManager(),
        EventManager(),
        SceneManager(),
        DisplayManager(),
    ]
    for element in loadinglist.loading_list:
        LOADERDICT['_loadlist'].append(element)

    

    