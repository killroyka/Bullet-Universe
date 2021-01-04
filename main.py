import pygame
import sys
import os
import math
from pprint import pprint
import random
from map import *


def draw_map(map):
    map_sprites = pygame.sprite.Group()
    pprint.pprint(map)
    for x in range(1, len(map) - 1):
        for y in range(1, len(map[x]) - 1):
            if map[y][x] == "#":
                Tile("wall_textures/black_wall.png", x, y, map_sprites)
            if map[y][x] == "L":
                Tile("wall_textures/side_wall.png", x, y, map_sprites, reverse_x=True)
            if map[y][x] == "R":
                Tile("wall_textures/side_wall.png", x, y, map_sprites)
            if map[y][x] == "D":
                Tile("wall_textures/up_wall.png", x, y, map_sprites)
            if map[y][x] == "U":
                Tile("wall_textures/up_wall.png", x, y, map_sprites, reverse_y=True)
    return map_sprites


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, group, reverse_x=False, reverse_y=False):
        super().__init__(group, all_sprites)
        self.image = load_image(image_name)
        self.image = pygame.transform.flip(self.image, reverse_x, reverse_y)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (pos_x * self.rect.size[0], pos_y * self.rect.size[1])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, angle, group, speed, whos):
        super().__init__(group, all_sprites)
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA)
        pygame.draw.circle(self.image, "red", (5, 5), 5)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = speed
        self.angle = angle
        self.whos = whos

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    image = load_image("spinbotAnimation/spinbot0.png")

    def __init__(self, pos_x, pos_y, angle, group):
        super().__init__(group, all_sprites)
        self.angle, self.group = angle, group
        self.image = Player.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 10
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


size = width, height = 1600, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
player = Player(500, 300, 0, player_sprites)
timer = 0
map_sprites = draw_map(map)
camera = Camera()
while True:
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in range(-4, 3):
                Bullet(player.rect.x + player.rect.size[0] // 2, player.rect.y + player.rect.size[1] // 2,
                       player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites,
                       random.randint(25, 30),
                       player)
    timer += 1
    timer = timer % 100
    if not pygame.sprite.spritecollideany(player, map_sprites):
        player_sprites.update()
    else:
        pass
        print(pygame.sprite.spritecollideany(player, map_sprites).rect.topright)
        player.rect.x = list(pygame.sprite.spritecollideany(player, map_sprites).rect.topright)[0]
        player.rect.y = list(pygame.sprite.spritecollideany(player, map_sprites).rect.topright)[1]
    bullet_sprites.update()
    map_sprites.draw(screen)
    all_sprites.draw(screen)
    camera.update(player)
    for x in map_sprites:
        pygame.sprite.spritecollide(x, bullet_sprites, True)
    bullet_sprites.draw(screen)
    for x in all_sprites:
        camera.apply(x)
    clock.tick(30)
    pygame.display.flip()
