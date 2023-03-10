import random
import pygame
import numpy as np
import pygame.gfxdraw

showGrades1 = False
showGrades2 = False


class Obj(pygame.sprite.Sprite):

    def __init__(self, img, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y


class Car(pygame.sprite.Sprite):

    def __init__(self, img, *groups):
        super().__init__(*groups)

        self.imgPicker = str(random.randint(0, 3))
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = 250
        self.rect[1] = 250
        self.ticks = 0
        self.vel = -8
        self.velHorizontal = 0
        self.grav = 1
        self.pts = 0
        self.play = True
        self.fitness = 0
        self.bird_earned_point = False

    def copy(self):
        new_car = Car("assets/bird" + self.imgPicker + "_0.png", self.groups())
        new_car.rect = self.rect.copy()
        new_car.ticks = self.ticks
        new_car.vel = self.vel
        new_car.velHorizontal = self.velHorizontal
        new_car.grav = self.grav
        new_car.pts = self.pts
        new_car.play = self.play
        new_car.fitness = self.fitness
        return new_car

    def update(self, *args):
        if self.play:
            self.anim()

        if self.rect[0] > -70:
            self.move()
        else:
            self.kill()

    def anim(self):
        self.ticks = (self.ticks + 1) % 4  # Vai fazer isso 6x depois voltar para 0
        self.image = pygame.image.load("assets/bird"+self.imgPicker+"_" + str(self.ticks) + ".png")

    def move(self):

        if self.play:
            self.fitness += 0.1

        self.vel += self.grav
        self.rect[1] += self.vel
        self.rect[0] += self.velHorizontal
        self.fitness += 0.1

        # Limitador de velocidade de queda e subida
        if self.vel >= 20:
            self.vel = 20
        if self.vel <= -10:
            self.vel = -10

        # bloqueio do passaro no chao e no teto
        if self.rect[1] >= 440:
            self.rect[1] = 440
        elif self.rect[1] <= 0:
            self.rect[1] = 0
            self.vel = 4

    def jump(self):
        self.vel -= 10

    def collision_sky(self):

        if self.rect[1] <= 0:
            self.play = False
            self.image = pygame.transform.rotate(self.image, 270)
            self.vel = 1
            self.velHorizontal = -4
            self.fitness -= 20

    def checkNewPoint(self, pipesTop_List, pipesBottom_List, actualPipe, window):

        if showGrades1:
            pygame.draw.line(window, (255, 0, 255), self.rect.center, pipesBottom_List[actualPipe].rect.midtop)
            pygame.draw.line(window, (255, 150, 0), self.rect.center, pipesTop_List[actualPipe].rect.midbottom)

        # Avalia se o retangulo do passaro está em contato com o retangulo de score
        if self.rect.clipline(pipesTop_List[actualPipe].rect.bottomright, pipesBottom_List[actualPipe].rect.topright):
            if not self.bird_earned_point:
                self.pts += 1
                self.bird_earned_point = True
        else:
            self.bird_earned_point = False

    def getDistance(self, pipesTop_List, pipesBottom_List, window):
        if self.play:
            actualPipe = 0
            if self.play and len(pipesTop_List) > 0:
                if pipesTop_List[0].rect.right < self.rect.left and pipesBottom_List[0].rect.right < self.rect.left:
                    actualPipe = 1
                self.distTop = (pipesTop_List[actualPipe].rect.bottom - self.rect.centery)
                self.distBottom = (pipesBottom_List[actualPipe].rect.top - self.rect.centery)
                self.distXToPipes = (pipesBottom_List[actualPipe].rect.left - self.rect.centerx)
                self.distHole = (pipesBottom_List[actualPipe].rect.centerx - self.rect.centerx)

            # Checa a pontuacao
            self.checkNewPoint(pipesTop_List, pipesBottom_List, actualPipe, window)


class Text:

    def __init__(self, size, text, font):
        pygame.font.init()
        self.font = pygame.font.Font("assets/font/"+font+".ttf", size)
        self.render = self.font.render(text, True, (0, 0, 0))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def text_update(self, text):
        self.render = self.font.render(text, True, (0, 0, 0))
