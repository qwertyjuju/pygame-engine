import pygame as pg

def main(sheight, swidth):
    pg.init()
    screen = pg.display.set_mode((sheight, swidth))
    surface = pg.image.load("data\\map\\gamemap.jpg").convert()
    pos=[0, 0]
    timer = pg.time.Clock()
    fpslist = []
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return fpslist
        screen.fill((0, 0, 0))
        screen.blit(surface, pos)
        pos[0]-=1
        pos[1]-=1
        pg.display.flip()
        timer.tick()
        fps = timer.get_fps()
        if len(fpslist) < 5000:
            fpslist.append(fps)
        else:
            pg.quit()
            return fpslist
        fps = str(fps)
        pg.display.set_caption(fps)


fpslist = main(1920, 1080)
sumfps = 0
for fps in fpslist:
    sumfps += fps
moyfps = sumfps / len(fpslist)
print(moyfps)

