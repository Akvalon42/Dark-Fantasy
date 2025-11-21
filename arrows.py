from constanta import *
import pygame as pg


class Arrow(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Arrow, self).__init__()

        self.direction = direction
        self.speed = 3

        self.image = pg.image.load("")
        self.image = pg.transform.scale(self.image, (12, 12))

        self.rect = self.image.get_rect()

        self.rect.x = player_rect.right if direction == "right" else player_rect.left
        self.rect.y = player_rect.centery
        # self.rect.center = player_rect.center


    def update(self):
        self.rect.x += self.speed if self.direction == "right" else -self.speed