"""
import pygame as pg
import sys


def main(sheight, swidth):
    pg.init()
    screen = pg.display.set_mode((sheight, swidth))
    timer = pg.time.Clock()
    fpslist = []
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return fpslist
        screen.fill((0, 0, 0))
        pg.display.flip()
        timer.tick()
        fps = timer.get_fps()
        if len(fpslist) < 1000:
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
