import pygame
import sys
import os
import math
from pprint import pprint
import random
from main import *


class Gun(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, angle, group):
        super().__init__(group, all_sprites)
        self.image = load_image(image_name)
        self.angle = angle
        self.coords = pos_x, pos_y

    def get_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect.x + self.rect.size[0] // 2), mouse_y - (
                self.rect.y + self.rect.size[1] // 2)
        self.angle = math.atan2(rel_y, rel_x)
        return self.angle

    def update(self):
        self.image = pygame.transform.rotate(self.image, self.get_angle() / math.pi * 180)


class ShotGun(Gun):
    def shot(self):
        for x in range(-4, 3):
            Bullet(player.rect.x + player.rect.size[0] // 2, player.rect.y + player.rect.size[1] // 2,
                   player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites,
                   random.randint(25, 30),
                   player)
