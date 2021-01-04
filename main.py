import pygame
import sys
import os
import math
from pprint import pprint
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self):
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, angle, group, speed, whos):
        super().__init__(group, all_sprites)
        self.image = pygame.Surface([10, 10])
        pygame.draw.circle(self.image, "red", (5, 5), 5)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = speed
        self.angle = angle
        self.whos = whos

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)


class Player(pygame.sprite.Sprite):
    image = load_image("spinbotAnimation/spinbot0.png")

    def __init__(self, pos_x, pos_y, angle, group):
        super().__init__(group, all_sprites)
        self.angle, self.group = angle, group
        self.image = Player.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect.x + self.rect.size[0] // 2), mouse_y - (
                    self.rect.y + self.rect.size[1] // 2)
        self.angle = math.atan2(rel_y, rel_x)

        keys = pygame.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        if keys[pygame.K_w]:
            self.rect.y += -self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x += -self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed


size = width, height = 1080, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
player = Player(500, 100, 0, player_sprites)
timer = 0
while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in range(-4, 3):
                Bullet(player.rect.x + player.rect.size[0] // 2, player.rect.y + player.rect.size[1] // 2,
                       player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites, random.randint(10, 15),
                       player)
    timer += 1
    timer = timer % 100
    player_sprites.update()
    bullet_sprites.update()
    bullet_for_del = []
    bullet_for_del.clear()
    all_sprites.draw(screen)
    clock.tick(60)

    pygame.display.flip()
