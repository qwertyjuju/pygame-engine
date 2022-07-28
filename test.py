import pathlib
import pygame as pg
import json

def main(sheight, swidth):
    pg.init()
    screen = pg.display.set_mode((sheight, swidth))
    surface = pg.image.load("data/map/gamemap.jpg").convert_alpha()
    #surface =surface.convert()
    pos=[0, 0]
    timer = pg.time.Clock()
    fpslist = []
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return fpslist
        screen.fill((0, 0, 0))
        pos[0]-=1
        pos[1]-=1
        #screen.fill((0, 0, 0), (100, 100, 200, 200))
        #screen.fill((0, 0, 0), (200, 200, 300, 300))
        #screen.fill((0, 0, 0), (300, 300, 400, 400))
        #screen.fill((0, 0, 0), (400, 400, 500, 500))
        screen.blit(surface, pos)
        #pos[0]-=1
        #pos[1]-=1
        pg.display.flip()
        timer.tick_busy_loop()
        fps = timer.get_fps()
        if len(fpslist) < 5000:
            fpslist.append(fps)
        else:
            pg.quit()
            return fpslist
        fps = str(fps)
        pg.display.set_caption(fps)


fpslist = main(1800, 1024)
sumfps = 0
for fps in fpslist:
    sumfps += fps
moyfps = sumfps / len(fpslist)
print(moyfps)

"""
class B:
    test = None
    def __init_subclass__(cls, **kwargs):
        cls.init_class()

    @classmethod
    def init_class(cls):
        pass

class A(B):

    @classmethod
    def init_class(cls):
        cls.test="test"

class C(A):
    pass


class D(C):
    pass

print(C.test)
"""

"""
from pathlib import Path

a=Path("data/map/test")
b = a.joinpath("../..")
print(a.exists())
print(b.parent)
"""

"""
def main(sheight, swidth):
    pg.init()
    screen = pg.display.set_mode((sheight, swidth))
    surface = pg.image.load("data\\map\\gamemap.jpg").convert_alpha()
    #surface =surface.convert()
    pos=[0, 0]
    timer = pg.time.Clock()
    fpslist = []
    while True:
        for event in pg.event.get():
            evname = pg.event.event_name(event.type)
            print(evname)
            if event.type == pg.QUIT:
                pg.quit()
                return fpslist
        screen.fill((0, 0, 0))
        #screen.fill((0, 0, 0), (100, 100, 200, 200))
        #screen.fill((0, 0, 0), (200, 200, 300, 300))
        #screen.fill((0, 0, 0), (300, 300, 400, 400))
        #screen.fill((0, 0, 0), (400, 400, 500, 500))
        screen.blit(surface, pos)
        #pos[0]-=1
        #pos[1]-=1
        pg.display.flip()
        timer.tick_busy_loop()
        fps = timer.get_fps()
        if len(fpslist) < 5000:
            fpslist.append(fps)
        else:
            pg.quit()
            return fpslist
        fps = str(fps)
        pg.display.set_caption(fps)


fpslist = main(1800, 1024)
sumfps = 0
for fps in fpslist:
    sumfps += fps
moyfps = sumfps / len(fpslist)
print(moyfps)
"""