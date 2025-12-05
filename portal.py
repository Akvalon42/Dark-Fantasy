import pygame as pg
from constanta import *
class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Portal, self).__init__()
        self.load_animations()
        self.image = self.images[0]
        self.rect = self.image.get_rect(x=x*TILE_SCALE, bottom=y*TILE_SCALE)
        self.mask = pg.mask.from_surface(self.image)
        self.current_image = 0
        self.interval = 100
        self.timer = pg.time.get_ticks()

    def load_animations(self):
        tile_size = 64
        tile_scale = 2
        self.images= []

        num_images = 8
        spriteSheet = pg.image.load("sprites/portals/Purple Portal Sprite Sheet.png").convert_alpha()

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spriteSheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            image = pg.transform.flip(image, False, True)
            self.images.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]
            self.timer = pg.time.get_ticks()