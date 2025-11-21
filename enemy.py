import pygame as pg


from constanta import *

class Enemy(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, start_pos, final_pos, spritesheet, num_images):
        super(Enemy, self).__init__()

        self.load_animations(spritesheet, num_images)

        self.current_animation = self.move_animations_left
        self.image = self.current_animation[0]
        self.current_image = 0
        self.direction = "left"

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos # Начальное положение персонажа
        self.left_edge = start_pos[0]
        self.right_edge = final_pos[0] + self.image.get_width()

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200



    def load_animations(self, spritesheet, num_images):
        tile_size_w = 64
        tile_size_h = 32
        tile_scale = 2
        self.move_animations_left = []

        for i in range(num_images):
            x = i * tile_size_w
            y = 0
            rect = pg.Rect(x, y, tile_size_w, tile_size_h)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size_w * tile_scale, tile_size_h * tile_scale))
            self.move_animations_left.append(image)

        self.move_animations_right = [pg.transform.flip(image, True, False) for image in self.move_animations_left]



    def update(self, platforms):

        if self.direction == "right":
            self.velocity_x = VELOCITY_ENEMY
            if self.rect.right >= self.right_edge:
                self.direction = "left"
                self.current_animation = self.move_animations_left
        elif self.direction == "left":
            self.velocity_x = -VELOCITY_ENEMY
            if self.rect.left <= self.left_edge:
                self.direction = "right"
                self.current_animation = self.move_animations_right
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

class Orc(Enemy):
    def __init__(self, map_width, map_height, start_pos, final_pos):
        spritesheet = pg.image.load("sprites/enemies/orc.png")
        super(Orc, self).__init__( map_width, map_height, start_pos, final_pos, spritesheet, 12)