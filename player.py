from arrows import Arrow
from constanta import *
import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, arrows, all_sprites):
        super(Player, self).__init__()

        self.load_animations()
        self.load_sounds()
        self.current_animation = self.idle_animations_right
        self.image = self.current_animation[0]
        self.current_image = 0
        self.direction = "right"
        self.rect = self.image.get_rect()
        self.arrows = arrows
        self.all_sprites = all_sprites
        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1

        self.is_jumping = False

        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

        self.hp = 5
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000
        self.arrow_timer = pg.time.get_ticks()
        self.arrow_interval = 1500
        self.hitbox = pg.Rect(self.rect.x, self.rect.y, 16 * TILE_SCALE, 16 * TILE_SCALE * 1.5 + 8 )

    def load_sounds(self):
        self.sound_steps = pg.mixer.Sound("sounds/Valley of Dreams.wav")
        self.sound_steps.set_volume(0.02)
        self.sound_bow = pg.mixer.Sound("sounds/a-shot-arrow-from-a-bow.wav")
        self.sound_bow.set_volume(0.2)
    def load_animations(self):
        tile_size = 32
        tile_scale = TILE_SCALE * 3.5

        self.idle_animations_right = []
        num_images = 4
        for i in range(1, num_images + 1):
            image = pg.image.load(f"sprites/idle_Hobbit/Hobbit - Idle{i}.png")
            image = pg.transform.scale(image, (tile_size * tile_scale ,tile_size * tile_scale))
            self.idle_animations_right.append(image)
        self.idle_animations_left = [pg.transform.flip(image, True, False) for image in self.idle_animations_right]

        self.move_animations_right = []
        num_images = 10
        for i in range(1, num_images + 1):
            image = pg.image.load(f"sprites/move_Hobbit/Hobbit - run{i}.png")
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.move_animations_right.append(image)
        self.move_animations_left = [pg.transform.flip(image, True, False) for image in self.move_animations_right]

        self.attack_animations_right = []
        num_images = 17
        for i in range(1, num_images + 1):
            image = pg.image.load(f"sprites/attack_Hobbit/Hobbit - attack{i}.png")
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.attack_animations_right.append(image)
        self.attack_animations_left = [pg.transform.flip(image, True, False) for image in self.attack_animations_right]

    def jump(self):
        self.velocity_y = -17
        self.is_jumping = True
    def update(self, platforms):
        keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE]and not self.is_jumping:
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_a]:
            # if self.current_image == 1:
            self.sound_steps.play()
            if self.current_animation != self.move_animations_left:
                self.current_animation = self.move_animations_left
                self.current_image = 0
                self.direction = "left"
            self.velocity_x = -5
        elif keys[pg.K_d]:
            # if self.current_image == 1:
            self.sound_steps.play()
            if self.current_animation != self.move_animations_right:
                self.current_animation = self.move_animations_right
                self.current_image = 0
                self.direction = "right"
            self.velocity_x = 5
        else:
            if self.current_animation == self.move_animations_right:
                self.current_animation = self.idle_animations_right
                self.current_image = 0
            elif self.current_animation == self.move_animations_left:
                self.current_animation = self.move_animations_left
                self.current_image = 0
            self.velocity_x = 0
        new_x = self.hitbox.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.hitbox.width:
            self.hitbox.x = new_x
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y

        mouse_keys = pg.mouse.get_pressed()
        if mouse_keys[0]:
            if pg.time.get_ticks() - self.arrow_timer > self.arrow_interval and self.current_image >= 11:
                self.sound_steps.stop()
                self.sound_bow.play()
                arrow = Arrow(self.hitbox, self.direction)
                self.arrows.add(arrow)
                self.all_sprites.add(arrow)
                self.arrow_timer = pg.time.get_ticks()


            if self.direction == "right":
                self.current_animation = self.attack_animations_right
            else:
                self.current_animation = self.attack_animations_left
        else:
            if self.direction == "right":
                self.current_animation = self.move_animations_right
            else:
                self.current_animation = self.move_animations_left

        for platform in platforms:
            if platform.rect.collidepoint(self.hitbox.midbottom):
                self.hitbox.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
                # print(platform)
            if platform.rect.collidepoint(self.hitbox.midtop):
                self.hitbox.top = platform.rect.bottom
                self.velocity_y = 0
                # print(platform)
            if platform.rect.collidepoint(self.hitbox.midright):
                self.hitbox.right = platform.rect.left
                # print(platform)
            if platform.rect.collidepoint(self.hitbox.midleft):
                self.hitbox.left = platform.rect.right
                # print(platform)

        self.rect.center = (self.hitbox.centerx, self.hitbox.centery + 4)


        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()
    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()