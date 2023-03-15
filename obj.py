import math
import random

import numpy as np
import pygame
import pygame.gfxdraw
import configparser
config = configparser.ConfigParser()
config.read('config.properties')

showGrades1 = False #config.get('pygame', 'showlines')


def draw_lines_to_edge(screen, matrizPixels, colorLine, x1, y1, angle):
    x2 = x1 + 5000 * math.cos(angle * math.pi / 180)
    y2 = y1 - 5000 * math.sin(angle * math.pi / 180)
    dx = x2 - x1
    dy = y2 - y1

    # Normalizar a direção da linha
    length = max(abs(dx), abs(dy))
    dx /= length
    dy /= length

    # Verificar cada pixel ao longo da trajetória da linha até encontrar um pixel preto
    x, y = x1, y1
    while True:
        # Verificar se estamos fora da tela
        if x < 0 or y < 0 or x >= screen.get_width() or y >= screen.get_height():
            break
        # Verificar se este pixel é preto
        if matrizPixels[(int(x), int(y))] != 4285756275:
            break
        # Avançar para o próximo pixel
        x += dx
        y += dy

    # Desenhar a linha até o primeiro pixel preto encontrado
    if showGrades1:
        pygame.draw.line(screen, colorLine, (x1, y1), (x, y), 1)

    return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)


def drawAllLines(screen, matrizPixels, carx, cary, car_angle):
    distances = [draw_lines_to_edge(screen, matrizPixels, (255, 255, 0), carx, cary, car_angle + 270),
                 draw_lines_to_edge(screen, matrizPixels, (0, 12, 255), carx, cary, car_angle + 305),
                 draw_lines_to_edge(screen, matrizPixels, (255, 102, 0), carx, cary, car_angle + 345),
                 draw_lines_to_edge(screen, matrizPixels, (255, 255, 255), carx, cary, car_angle),
                 draw_lines_to_edge(screen, matrizPixels, (102, 51, 0), carx, cary, car_angle + 15),
                 draw_lines_to_edge(screen, matrizPixels, (0, 102, 255), carx, cary, car_angle + 45),
                 draw_lines_to_edge(screen, matrizPixels, (255, 51, 204), carx, cary, car_angle + 90)]
    return distances


class Obj(pygame.sprite.Sprite):

    def __init__(self, img, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y


class Car(pygame.sprite.Sprite):

    def __init__(self, img, matrizPixels, matrizCusto, *groups):
        super().__init__(*groups)

        self.imgPicker = str(random.randint(0, 1))
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = 315
        self.rect[1] = 415
        self.angle = 0
        self.ticks = 0
        self.speed = 3
        self.play = True
        self.fitness = 0
        self.distances = []
        self.matrizPixels = matrizPixels
        self.matrizCusto = matrizCusto
        self.restoY = 0
        self.restoX = 0

    def copy(self):
        new_car = Car("assets/car" + self.imgPicker + "_0.png", self.groups())
        new_car.rect = self.rect.copy()
        new_car.angle = self.angle
        new_car.ticks = self.ticks
        new_car.speed = self.speed
        new_car.play = self.play
        new_car.fitness = self.fitness
        new_car.distances = self.distances
        new_car.matrizPixels = self.matrizPixels
        new_car.matrizCusto = self.matrizCusto
        return new_car

    def update(self, window):

        self.ticks += 1

        if self.ticks >= 3000:
            self.matar_carro()

        if self.play:

            # Retorna o angulo real dentro dos 360
            self.angle %= 360

            # Converte o ângulo para radianos
            angle_rad = math.radians(self.angle)

            # Calcula a variação nas coordenadas x e y do retângulo
            delta_x = self.speed * math.cos(angle_rad)
            delta_y = self.speed * math.sin(angle_rad)

            # Atualiza as coordenadas x e y do retângulo
            self.rect[0] += round(delta_x) + self.restoX
            self.rect[1] += round(delta_y) + self.restoY

            # self.restoX = round(delta_x) - delta_x
            # self.restoY = round(delta_y) - delta_y

            # Gira o carro de acordo com a inclinacao
            self.rotateCar(window)

            # Caso o carro vá parar fora da pista
            if self.matrizCusto[self.rect.center] == 0:
                self.rect[0] -= round(delta_x)
                self.rect[1] -= round(delta_y)
                self.matar_carro()

    def rotateCar(self, window):

        # gira a imagem
        if self.speed != 0:
            img_copy = pygame.transform.rotate(self.image, self.angle * -1)
            self.distances = drawAllLines(window, self.matrizPixels,
                                          self.rect[0] - int(img_copy.get_width() / 2) + img_copy.get_width() / 2,
                                          self.rect[1] - int(img_copy.get_height() / 2) + + img_copy.get_height() / 2,
                                          self.angle * -1)

            if min(self.distances) <= (self.rect.height / 2):
                self.matar_carro()

            # Atualizar
            window.blit(img_copy, (self.rect[0] - int(img_copy.get_width() / 2), self.rect[1] - int(img_copy.get_height() / 2)))

    def atualiza_score(self):

        if not self.play:
            self.fitness = self.matrizCusto[self.rect.center]

    def matar_carro(self):
        self.play = False
        self.speed = 0
        self.atualiza_score()


class Text:

    def __init__(self, size, text, font, x, y):
        pygame.font.init()
        self.x = x
        self.y = y
        self.font = pygame.font.Font("assets/font/" + font + ".ttf", size)
        self.render = self.font.render(text, True, (255, 255, 255))

    def draw(self, window):
        window.blit(self.render, (self.x, self.y))

    def text_update(self, text):
        self.render = self.font.render(text, True, (255, 255, 255))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.pressedColor = (200, 200, 148)
        self.notPressedColor = (191, 191, 191)
        self.fontPressedColor = (230, 230, 230)
        self.fontNotPressedColor = (255, 255, 255)
        self.text = text
        self.corner_radius = 10
        self.pressed = False
        pygame.font.init()
        self.font = pygame.font.Font("assets/font/OpenSans-Regular.ttf", 20)

    def draw(self, surface):
        if self.pressed:
            self.color = self.pressedColor
            self.fontColor = self.fontPressedColor
        else:
            self.color = self.notPressedColor
            self.fontColor = self.fontNotPressedColor

        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.corner_radius)
        text = self.font.render(self.text, True, self.fontColor)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            global showGrades1
            showGrades1 = not showGrades1
            self.pressed = not self.pressed


class Chart:

    def __init__(self, x, y, height, width):

        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.chart_surface = None

    def update(self, generation, histY):

        generation -= 1

        if len(histY) > 0:
            # Generate random data points
            x = np.random.randint(1, 10, size=generation)
            y = histY

            # Calculate the maximum Y value
            max_y = max(y)

            if max_y > 0:
                # Draw the chart on a surface
                self.chart_surface = pygame.Surface((self.width, self.height))
                self.chart_surface.fill((33, 33, 33))

                for i in range(len(x) - 1):
                    x1 = round((i * self.width) / generation)
                    y1 = int(100 - (y[i] / max_y) * 80)
                    x2 = round(((i + 1) * self.width) / generation)
                    y2 = int(100 - (y[i + 1] / max_y) * 80)
                    pygame.gfxdraw.line(self.chart_surface, x1, y1, x2, y2, (255, 255, 255))

                # Draw a circle at each data point
                for i in range(len(x)):
                    x_pos = round((i * self.width) / generation)
                    y_pos = int(100 - (y[i] / max_y) * 80)
                    pygame.draw.circle(self.chart_surface, (255, 255, 255), (x_pos, y_pos), 3)

    def draw(self, window):

        if self.chart_surface is not None:
            # Blit the chart surface onto the main pygame window
            window.blit(self.chart_surface, (self.x, self.y))
