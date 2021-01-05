import pygame
import sys
import os
import math
from pprint import pprint
import random
from main import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Gun(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, angle, group):
        super().__init__(group, all_sprites)
        self.image = load_image(image_name)
        self.angle = angle
        self.coords = pos_x, pos_y


    def update(self, player):
        self.x, self.y = player.rect.centerx, player.rect.recty
        self.angle = player.angle
        self.image = pygame.transform.rotate(self.image, self.get_angle() / math.pi * 180)


class ShotGun(Gun):
    def shot(self):
        for x in range(-4, 3):
            Bullet(player.rect.x + player.rect.size[0] // 2, player.rect.y + player.rect.size[1] // 2,
                   player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites,
                   random.randint(25, 30),
                   player)
