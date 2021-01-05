import pygame
import sys
import os
import math
from pprint import pprint
import random
from map import *


def draw_map(map):
    map_sprites = pygame.sprite.Group()
    corner_sprites = pygame.sprite.Group()
    pprint.pprint(map)
    for x in range(1, len(map) - 1):
        for y in range(1, len(map[0]) - 1):
            if map[x][y] == "#" and map[x][y - 1] == ".":
                Tile("wall_textures/side_wall.png", y, x, map_sprites, reverse_x=True)
            if map[x][y] == "#" and map[x][y + 1] == ".":
                Tile("wall_textures/side_wall.png", y, x, map_sprites)
            if map[x][y] == "#" and map[x + 1][y] == ".":
                Tile("wall_textures/up_wall.png", y, x, map_sprites)
            if map[x][y] == "#" and map[x - 1][y] == ".":
                Tile("wall_textures/up_wall.png", y, x, map_sprites, reverse_y=True)

            if map[x][y] == "#" and map[x - 1][y - 1] == ".":
                Tile("wall_textures/LD_wall.png", y, x, corner_sprites)
            if map[x][y] == "#" and map[x - 1][y + 1] == ".":
                Tile("wall_textures/RD_wall.png", y, x, corner_sprites)
            if map[x][y] == "#" and map[x + 1][y - 1] == ".":
                Tile("wall_textures/UL_wall.png", y, x, corner_sprites)
            if map[x][y] == "#" and map[x + 1][y + 1] == ".":
                Tile("wall_textures/UR_wall.png", y, x, corner_sprites)
    for x in map_sprites:
        pygame.sprite.spritecollide(x, corner_sprites, True)
    for x in corner_sprites:
        map_sprites.add(corner_sprites)
    return map_sprites


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Spin_bot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, player):
        super().__init__(group, all_sprites)
        self.images = [load_image("spinbotAnimation/spinbotanimation_1.png"),
                       load_image("spinbotAnimation/spinbotanimation_2.png"),
                       load_image("spinbotAnimation/spinbotanimation_3.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = 9
        self.get_angle(player.rect.centerx, player.rect.centery)

    def get_angle(self, player_pos_x, player_pos_y):
        rel_x, rel_y = player_pos_x - self.rect.centerx, player_pos_y - self.rect.centery
        self.angle = math.atan2(rel_y, rel_x)

    def next_image(self):
        self.image = self.images[(self.images.index(self.image) + 1) % 3]

    def update(self, player):
        if timer % 7 == 0:
            self.next_image()
        self.get_angle(player.rect.centerx, player.rect.centery)
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, group, reverse_x=False, reverse_y=False):
        super().__init__(group, all_sprites)
        self.image = load_image(image_name)
        self.image = pygame.transform.flip(self.image, reverse_x, reverse_y)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (pos_x * self.rect.size[0], pos_y * self.rect.size[1])
        self.mask = pygame.mask.from_surface(self.image)


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
        print([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]].count(1))
        if [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]].count(1) == 2:
            self.speed = 7
        else:
            self.speed = 10
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
enemies_sprites = pygame.sprite.Group()
Spin_bot(500, 500, enemies_sprites, player)
while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in range(-4, 3):
                Bullet(player.rect.centerx, player.rect.centery,
                       player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites,
                       random.randint(25, 30),
                       player)
    timer += 1
    timer = timer % 1000
    if not pygame.sprite.spritecollideany(player, map_sprites):
        player_sprites.update()
    map_sprites.draw(screen)
    all_sprites.draw(screen)
    camera.update(player)
    bullet_sprites.draw(screen)
    bullet_sprites.update()
    enemies_sprites.update(player)
    for x in map_sprites:
        pygame.sprite.spritecollide(x, bullet_sprites, True)
    for x in all_sprites:
        camera.apply(x)
    clock.tick(30)
    pygame.display.flip()
