import os
import sys

import random

import pygame

size = width, height = 1200, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Running pudge')
pygame.time.set_timer(pygame.USEREVENT, 120)
clock = pygame.time.Clock()

pygame.init()

pygame.mixer.music.load('data/mus.mp3')
pygame.mixer.music.play(-1, 0.0, 10)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


img = load_image('icon.png', -1)
pygame.display.set_icon(img)


# Класс основного героя
class Pudge(pygame.sprite.Sprite):
    global his
    image = pygame.transform.scale(load_image('pudge1.png', -1), (100, 100))
    image2 = pygame.transform.scale(load_image('pudge2.png', -1), (100, 100))

    def __init__(self):
        super().__init__(sprt)
        self.image = Pudge.image
        self.pic = 1
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 460)


    # Анимация хождения
    def update(self):
        if self.pic % 2 == 1:
            self.image = Pudge.image2
            self.pic += 1
        else:
            self.image = Pudge.image
            self.pic += 1


def const():
    global walr
    walr = False

def gogo():
    global his
    his = False


# Класс препятсвий
class Walls(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('box.png', -1), (50, 80))
    global his

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Walls.image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


    def update(self):
        if pygame.sprite.spritecollideany(self, sprt):
            const()
            self.kill()
        else:
            self.rect.left -= 30



all_sprites = pygame.sprite.Group()
sprt = pygame.sprite.Group()


def start_screen():
    intro_text = ["                Running pugde", "",
                  "         Прыжок на кнопку space",
                  "      Пауза/продолжение трека: 'o'",
                  "         Увеличить громкость: 'p'",
                  "         Уменьшить громкость: 'i'", "",
                  "Нажмите любую клавишу, чтобы начать"]

    fon = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(30)


def terminate():
    pygame.quit()
    sys.exit()


start_screen()

Walls((1220, 460))

fon = pygame.transform.scale(load_image('fon2.jpg'), (width, height))

count = 0
hero = None
tid = 0
k = 0
nowtid = 0
walr = True
paus = False
vol = 0.8
herofl = True
vol1 = 80
his = False

font = pygame.font.SysFont('calibri', 62)
font1 = pygame.font.SysFont('calibri', 22)
font2 = pygame.font.SysFont('calibri', 16)
font4 = pygame.font.SysFont('calibri', 26)

text = font.render('Вы проиграли', 1, 'black')
text2 = font2.render('Сейчас играет: 78Pt - lowfreq', 1, 'black')
text4 = font4.render('Для повторного прохождения нажмите на f1', 1, 'black')


textflag = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                walr = True
                count = 0
                k = 0

            # Механики работы с музыкой
            elif event.key == pygame.K_o:
                paus = not paus
                if paus:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_i:
                if vol <= 0:
                    vol = 0.0
                else:
                    vol -= 0.1
                pygame.mixer.music.set_volume(vol)
            elif event.key == pygame.K_p:
                if vol >= 1:
                    vol = 1.0
                else:
                    vol += 0.1
                pygame.mixer.music.set_volume(vol)


        # Запуск игры
        if walr:
            textflag = False
            if event.type == pygame.USEREVENT:
                all_sprites.update()
                sprt.update()
                count += 1

                if herofl:
                    hero = Pudge()
                    herofl = False


                # Механика приземления персонажа
                if tid == 1:
                    if nowtid == 0:
                        nowtid = count
                    else:
                        if count == nowtid + 8:
                            hero.rect.top += 100
                            nowtid = 0
                            tid = False

                # Создание случайно расположенных препятсвий
                if count == k + 20:
                    kwall = random.randint(1, 4)
                    rnd = random.randint(1250, 1320)
                    if kwall == 1:
                        Walls((rnd, 460))
                    elif kwall == 2:
                        Walls((rnd, 460))
                        Walls((rnd + 50, 460))
                    elif kwall == 3:
                        Walls((rnd, 460))
                        Walls((rnd + 50, 460))
                        Walls((rnd + 100, 460))
                    k = count

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and hero.rect.top != 360:
                tid = 1
                hero.rect.top -= 100
        else:
            textflag = True

    screen.blit(fon, (0, 0))
    vol1 = (vol * 100) // 1
    text1 = font1.render(f'Счёт: {count}', 1, 'black')
    text5 = font4.render(f'Ваш счёт: {count}', 1, 'black')
    text3 = font2.render(f'Громкость: {vol1}%', 1, 'black')

    if textflag:
        screen.blit(text, (410, 220))
        screen.blit(text5, (485, 300))
        screen.blit(text4, (350, 350))
    else:
        screen.blit(text1, (10, 40))
    all_sprites.draw(screen)
    sprt.draw(screen)
    screen.blit(text2, (10, 10))
    screen.blit(text3, (10, 25))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
