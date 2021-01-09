import pygame
import sys
import os
import math
import pprint
import random
from map import *
from sounds import *
from time import sleep as sl


class Gun(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, angle, group):
        super().__init__(group, all_sprites)
        self.image = load_image(image_name)
        self.angle = angle
        self.coords = pos_x, pos_y
        self.last_angle = 0
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def rotate(self, img, pos, angle):
        w, h = img.get_size()
        img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img2.blit(img, (w - pos[0], h - pos[1]))
        return pygame.transform.rotate(img2, angle)

    def update(self, player):
        self.image = self.rotate(self.image, player.rect.center, player.angle - self.last_angle / math.pi * 180)
        self.last_angle = player.angle


class ShotGun(Gun):
    def shot(self):
        for x in range(-4, 3):
            Bullet(player.rect.x + player.rect.size[0] // 2, player.rect.y + player.rect.size[1] // 2,
                   player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites,
                   random.randint(25, 30),
                   player)


def draw_map(map):
    map_sprites = pygame.sprite.Group()
    corner_sprites = pygame.sprite.Group()
    for x in range(len(map) - 1):
        for y in range(len(map[0]) - 1):
            if map[x][y] == "e":
                Enemy(128 * y, 128 * x, enemies_sprites, player)
            if map[x][y] == "#" and map[x][y - 1] != "#":
                Tile("wall_textures/side_wall.png", y, x, map_sprites, reverse_x=True)
            if map[x][y] == "#" and map[x][y + 1] != "#":
                Tile("wall_textures/side_wall.png", y, x, map_sprites)
            if map[x][y] == "#" and map[x + 1][y] != "#":
                Tile("wall_textures/up_wall.png", y, x, map_sprites)
            if map[x][y] == "#" and map[x - 1][y] != "#":
                Tile("wall_textures/up_wall.png", y, x, map_sprites, reverse_y=True)

            if map[x][y] == "#" and map[x - 1][y - 1] != "#":
                Tile("wall_textures/LD_wall.png", y, x, corner_sprites)
            if map[x][y] == "#" and map[x - 1][y + 1] != "#":
                Tile("wall_textures/RD_wall.png", y, x, corner_sprites)
            if map[x][y] == "#" and map[x + 1][y - 1] != "#":
                Tile("wall_textures/UL_wall.png", y, x, corner_sprites)
            if map[x][y] == "#" and map[x + 1][y + 1] != "#":
                Tile("wall_textures/UR_wall.png", y, x, corner_sprites)
    for x in map_sprites:
        pygame.sprite.spritecollide(x, corner_sprites, True)
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


def draw_FPS(screen):
    font = pygame.font.Font(None, 50)
    text = font.render(str(int(clock.get_fps())), True, (100, 255, 100))
    text_x = size[0] - text.get_width()
    screen.blit(text, (text_x, 0))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, player, speed=10, hp=100):
        super().__init__(group, all_sprites)
        self.images = [load_image("spinbotAnimation/spinbotanimation_1.png"),
                       load_image("spinbotAnimation/spinbotanimation_2.png"),
                       load_image("spinbotAnimation/spinbotanimation_3.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.speed = speed
        self.get_angle()
        self.collision = [0, 0, 0, 0]
        self.map = []
        self.hp = hp
        for x in range(len(map)):
            self.map.append([])
            for y in range(len(map[x])):
                self.map[x].append(map[x][y])
        self.way = []
        self.playerx = (player.rect.centery - camera.ddx) // 128
        self.playery = (player.rect.centerx - camera.ddy) // 128
        self.map[self.rect.y // 128][self.rect.x // 128] = 0
        print([[self.rect.x // 128], [self.rect.y // 128]])

        self.t = 0

    def get_angle(self):
        mouse_x, mouse_y = player.rect.centerx, player.rect.centery
        rel_y, rel_x = mouse_x - (self.rect.x + self.rect.size[0] // 2), mouse_y - (
                self.rect.y + self.rect.size[1] // 2)
        self.angle = -math.atan2(rel_y, rel_x) + math.pi / 2

    def next_image(self):
        self.image = self.images[(self.images.index(self.image) + 1) % 3]

    def update_way(self):
        self.map = []
        for x in range(len(map)):
            self.map.append([])
            for y in range(len(map[x])):
                self.map[x].append(map[x][y])
        self.map[self.rect.y // 128][self.rect.x // 128] = 0

        d = 0
        self.way = []
        self.t = 0
        self.playerx = (player.rect.centery - camera.ddy) // 128
        self.playery = (player.rect.centerx - camera.ddx) // 128
        self.map[self.playerx][self.playery] = "p"
        self.map[self.rect.centery // 128][self.rect.centerx // 128] = 0

        while self.map[self.playerx][self.playery] == "p":

            for x in range(1, len(self.map)):
                for y in range(1, len(map[0])):
                    try:
                        if self.map[x - 1][y] == "#" and self.map[x + 1][y] == "#" and self.map[x][y - 1] == "#" and \
                                self.map[x][y + 1] == "#":
                            break
                    except Exception:
                        print("error")
                    if self.map[x][y] == d:
                        if self.map[x - 1][y] != "#" and type(self.map[x - 1][y]) != type(0):
                            self.map[x - 1][y] = self.map[x][y] + 1
                        if self.map[x + 1][y] != "#" and type(self.map[x + 1][y]) != type(0):
                            self.map[x + 1][y] = self.map[x][y] + 1
                        if self.map[x][y - 1] != "#" and type(self.map[x][y - 1]) != type(0):
                            self.map[x][y - 1] = self.map[x][y] + 1
                        if self.map[x][y + 1] != "#" and type(self.map[x][y + 1]) != type(0):
                            self.map[x][y + 1] = self.map[x][y] + 1
            d += 1

        x = self.playerx
        y = self.playery
        while d > 0:
            a = d
            if self.map[x + 1][y] == d:
                self.way.append([x + 1, y])
                x += 1
                d -= 1
            if self.map[x - 1][y] == d:
                self.way.append([x - 1, y])
                x -= 1
                d -= 1
            if self.map[x][y + 1] == d:
                self.way.append([x, y + 1])
                y += 1
                d -= 1
            if self.map[x][y - 1] == d:
                self.way.append([x, y - 1])
                y -= 1
                d -= 1
            if a == d:
                break

        self.way = [[self.playerx, self.playery]] + self.way
        self.map[self.playerx][self.playery] = '.'

    def update(self, player):
        self.get_angle()
        check = [0, 0, 0]
        ax = self.rect.centerx
        ay = self.rect.centery
        for x in range(0, 1000, 10):
            ax += self.speed * math.cos(self.angle)
            ay += self.speed * math.sin(self.angle)
            if player.rect.collidepoint(ax, ay):
                check[0] = 1
                break
            for y in map_sprites:
                if y.rect.collidepoint(ax, ay):
                    check[2] = 1
                    break
            else:
                continue
            break
        self.collision = check
        if check[1]:

            if self.t >= len(self.way):
                self.update_way()
            if self.rect.centerx // 128 != self.way[self.t][0] or self.rect.centery // 128 != self.way[self.t][1]:
                self.rect.centerx -= (self.rect.centerx // 128 - self.way[self.t][0]) * (self.speed // 2)
                self.rect.centery -= (self.rect.centery // 128 - self.way[self.t][1]) * (self.speed // 2)
            if self.rect.x // 128 == self.playerx and self.rect.y // 128 == self.playery:
                self.update_way()
            else:
                self.t += 1

        if check[0]:
            self.rect.x += self.speed * math.cos(self.angle)
            self.rect.y += self.speed * math.sin(self.angle)


class Spin_bot(Enemy):
    def __init__(self, pos_x, pos_y, group, player, speed=10):
        super().__init__(pos_x, pos_y, group, player, speed=10)
        self.form = 0

    def circle_shoot(self):
        for x in range(0, 13, 1):
            Bullet(self.rect.centerx + 40 * math.cos(x / 2), self.rect.centery + 40 * math.sin(x / 2), self.angle,
                   bullet_sprites, 10,
                   "enemy")

    def transform(self):
        if self.form == 1 and self.images.index(self.image) != 2:
            self.image = self.images[self.images.index(self.image) + 1]
            self.speed = 0
        elif self.form == 0 and self.images.index(self.image) != 0:
            self.image = self.images[self.images.index(self.image) - 1]
            self.speed = 0

    def update(self, player):
        super().update(player)
        print(((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2) ** 0.5)
        if ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2) ** 0.5 < 700 and self.collision[0]:
            self.speed = 0
            self.form = 1
            self.transform()
        elif self.collision[0]:
            self.form = 0
            self.transform()
        if self.images.index(self.image) == 2:
            self.speed = 5
        else:
            self.speed = 10
        if timer % 50 == 0 and self.form == 1:
            self.circle_shoot()


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, group, reverse_x=False, reverse_y=False):
        super().__init__(group, all_sprites)
        self.reverse_y = reverse_y
        self.reverse_x = reverse_x
        self.image_name = image_name
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
        self.ddx = 0
        self.ddy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        self.ddx += self.dx
        self.ddy += self.dy


class Player(pygame.sprite.Sprite):
    image = load_image("spinbotAnimation/spinbot0.png")

    def __init__(self, pos_x, pos_y, angle, group):
        super().__init__(group, all_sprites)
        self.hp = 100
        self.dmg = 10
        self.angle, self.group = angle, group
        self.image = Player.image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.reloading = 100
        self.speed = 40
        self.mask = pygame.mask.from_surface(self.image)

    def draw_hp_reloading(self):
        pygame.draw.rect(screen, (103, 6, 6), (0, 0, self.hp * width // 200, height // 40))
        pygame.draw.rect(screen, (6, 22, 103), (width // 2, 0,  self.reloading * width // 200, height // 40))
    def update(self):
        self.draw_hp_reloading()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect.x + self.rect.size[0] // 2), mouse_y - (
                self.rect.y + self.rect.size[1] // 2)
        self.angle = math.atan2(rel_y, rel_x)
        keys = pygame.key.get_pressed()
        collision = [0, 0, 0, 0]
        for x in map_sprites:
            j = pygame.sprite.collide_mask(self, x)
            if j:
                if x.image_name == "wall_textures/up_wall.png" and not x.reverse_y:
                    collision[0] = 1
                if x.image_name == "wall_textures/up_wall.png" and x.reverse_y:
                    collision[1] = 1
                if x.image_name == "wall_textures/side_wall.png" and not x.reverse_x:
                    collision[2] = 1
                if x.image_name == "wall_textures/side_wall.png" and x.reverse_x:
                    collision[3] = 1
        if [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]].count(1) == 2:
            self.speed = (self.speed ** 2) ** 0.5
        else:
            self.speed = 10
        if keys[pygame.K_w] and not collision[0]:
            self.rect.y += -self.speed
        if keys[pygame.K_s] and not collision[1]:
            self.rect.y += self.speed
        if keys[pygame.K_a] and not collision[2]:
            self.rect.x += -self.speed
        if keys[pygame.K_d] and not collision[3]:
            self.rect.x += self.speed


pygame.init()
size = width, height = 1600, 1080
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
player = Player(500, 500, 0, player_sprites)
timer = 0
camera = Camera()
enemies_sprites = pygame.sprite.Group()
enemy = Spin_bot(800, 1400, enemies_sprites, player, 10)

map_sprites = draw_map(map)

guns_sprites = pygame.sprite.Group()

# саундтрек
pygame.mixer.music.load('data/sounds/soundtrack.wav')
pygame.mixer.music.play(-1)
#
sounds = Sounds()
shot_timer = 0
while True:
    screen.fill("black")
    for event in pygame.event.get():
        for x in enemy.way:
            enemy.map[x[0]][x[1]] = "w"
        if event.type == pygame.QUIT:
            for t in range(len(enemy.map)):
                for z in range(len(enemy.map[0])):
                    print(map[t][z], end="\t")
                print()
            print(enemy.way)

            exit()

    timer += 1
    timer = timer % 1000
    all_sprites.draw(screen)
    player_sprites.update()

    camera.update(player)
    bullet_sprites.update()
    guns_sprites.update(player)
    enemies_sprites.update(player)
    draw_FPS(screen)

    if pygame.mouse.get_pressed(3)[0] and shot_timer >= 50:
        for x in range(-4, 3):
            Bullet(player.rect.centerx, player.rect.centery,
                   player.angle + (x * random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06])), bullet_sprites,
                   random.randint(25, 30),
                   "player")
            sounds.shotgun_shot()
            shot_timer = 0
    shot_timer += 1
    for x in bullet_sprites:
        if pygame.sprite.collide_mask(player, x) and x.whos != "player":
            pygame.sprite.spritecollide(player, bullet_sprites, True)
            player.hp -= 10
            player.update()
            draw_FPS(screen)
        for y in enemies_sprites:
            if pygame.sprite.collide_mask(x, y) and x.whos != "enemy":
                y.hp -= player.dmg
                pygame.sprite.spritecollide(y, bullet_sprites, True)
                if y.hp <= 0:
                    #TODO нарисовать сломанного бота
                    y.image = load_image("magnum.png")
                    enemies_sprites.remove(y)

    for x in map_sprites:
        j = pygame.sprite.spritecollide(x, bullet_sprites, True)
    for x in all_sprites:
        camera.apply(x)
    clock.tick(60)
    pygame.display.flip()
