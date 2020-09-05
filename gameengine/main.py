import sys
import pygame as pg
import common


class Engine:
    def __init__(self, **gameinfo):
        pg.init()
        common.initialize()
    
    def run(self):
        self.clock = pg.time.Clock()
        while common.GAMERUNNING:
            for manager in common.MANAGERS:
                manager.run()
            self.clock.tick()
            common.CURRENTFPS = self.clock.get_fps()
        pg.quit()
        sys.exit()
