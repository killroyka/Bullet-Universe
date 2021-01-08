import pygame
import sys
import os
import math
from pprint import pprint
import random
from map import *
from sounds import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit


class Gun(pygame.sprite.Sprite):
    def __init__(self, image_name, pos_x, pos_y, group):
        super().__init__(group, all_sprites)
        self.image = load_image(image_name)
        self.coords = pos_x, pos_y
        self.last_angle = 0
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self, player):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.coords[0], mouse_y - self.coords[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        self.rect = self.image.get_rect(center=(player.rect.x, player.rect.y))


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
            self.speed = 7
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


def game():
    global all_sprites, player_sprites, bullet_sprites, timer, guns_sprites, map_sprites, enemies_sprites, camera, player, clock, size, width, height
    size = width, height = 1600, 1080
    pygame.init()
    timer = 0
    shot_timer = 0
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    player = Player(500, 300, 0, player_sprites)

    camera = Camera()
    enemies_sprites = pygame.sprite.Group()
    Spin_bot(500, 500, enemies_sprites, player)

    map_sprites = draw_map(map)

    guns_sprites = pygame.sprite.Group()

    # саундтрек
    pygame.mixer.music.load('data/sounds/soundtrack.wav')
    pygame.mixer.music.play(-1)
    #
    sounds = Sounds()
    gun = ShotGun('magnum.png', player.rect.centerx, player.rect.centery, guns_sprites)
    while True:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        timer += 1
        timer = timer % 1000
        player_sprites.update()
        all_sprites.draw(screen)
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
                       player)
                sounds.shotgun_shot()
                shot_timer = 0
        shot_timer += 1
        for x in map_sprites:
            j = pygame.sprite.spritecollide(x, bullet_sprites, True)
        for x in all_sprites:
            camera.apply(x)
        clock.tick(60)
        pygame.display.flip()


class Example(QWidget):
    def __init__(self):
        self.count = 0
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 400)
        self.setWindowTitle('Фокус со словами')
        self.btn_play = QPushButton('Играть', self)
        self.btn_play.resize(200, 40)
        self.btn_play.move(10, 20)
        self.btn_play.clicked.connect(self.play)
        self.btn_settings = QPushButton('Настройки', self)
        self.btn_settings.resize(200, 40)
        self.btn_settings.move(10, 70)
        self.btn_settings.clicked.connect(self.settings)
        self.btn_exit = QPushButton('Выйти', self)
        self.btn_exit.resize(200, 40)
        self.btn_exit.move(10, 120)
        self.btn_exit.clicked.connect(self.exit)

    def play(self):
        game()

    def settings(self):
        pass

    def exit(self):
        exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
