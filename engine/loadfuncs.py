import json


def load_json(path):
    with path.open('r') as file:
        data = json.load(file)
    return data


def load_img(path):
    return GameImage(path)


class GameImage:
    image = None

    def __init__(self, imageloc):
        self.loc = imageloc
        self.load()

    def load(self):
        self.surface = pg.image.load(self.loc).convert_alpha()

    def get_tile(self, x, y, size):
        newsurf = pg.Surface(size, pg.SRCALPHA).convert_alpha()
        newsurf.blit(self.image, (-x, -y))
        return newsurf

    def get_surface(self):
        return self.surface


LOADFUNCS={
    ".json": load_json,
    ".png": load_img,
    ".jpg": load_img,
    ".world": load_json
}