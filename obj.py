import math
import random
import pygame
import pygame.gfxdraw

showGrades1 = False


def draw_lines_to_edge(screen, colorLine, x1, y1, angle):
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
        color = screen.get_at((int(x), int(y)))
        if color == (0, 0, 0, 255):
            break
        # Avançar para o próximo pixel
        x += dx
        y += dy

    # Desenhar a linha até o primeiro pixel preto encontrado
    if showGrades1:
        pygame.draw.line(screen, colorLine, (x1, y1), (x, y), 1)

    return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)


def drawAllLines(screen, carx, cary, car_angle):
    distances = [draw_lines_to_edge(screen, (255, 255, 0), carx, cary, car_angle + 270),
                 draw_lines_to_edge(screen, (0, 12, 255), carx, cary, car_angle + 305),
                 draw_lines_to_edge(screen, (255, 102, 0), carx, cary, car_angle + 345),
                 draw_lines_to_edge(screen, (102, 255, 153), carx, cary, car_angle),
                 draw_lines_to_edge(screen, (102, 51, 0), carx, cary, car_angle + 15),
                 draw_lines_to_edge(screen, (0, 102, 255), carx, cary, car_angle + 45),
                 draw_lines_to_edge(screen, (255, 51, 204), carx, cary, car_angle + 90)]
    return distances


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

        self.imgPicker = str(random.randint(0, 1))
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = 350
        self.rect[1] = 415
        self.angle = 0
        self.ticks = 0
        self.speed = 1
        self.score = 0
        self.play = True
        self.fitness = 0
        self.distances = []

    def copy(self):
        new_car = Car("assets/car" + self.imgPicker + "_0.png", self.groups())
        new_car.rect = self.rect.copy()
        new_car.angle = self.angle
        new_car.ticks = self.ticks
        new_car.speed = self.speed
        new_car.score = self.score
        new_car.play = self.play
        new_car.fitness = self.fitness
        new_car.distances = self.distances
        return new_car

    def update(self, window):

        if self.play:
            # Retorna o angulo real dentro dos 360
            self.angle %= 360

            # Converte o ângulo para radianos
            angle_rad = math.radians(self.angle)

            # Calcula a variação nas coordenadas x e y do retângulo
            delta_x = self.speed * math.cos(angle_rad)
            delta_y = self.speed * math.sin(angle_rad)

            # Atualiza as coordenadas x e y do retângulo
            self.rect[0] += delta_x
            self.rect[1] += delta_y

            # Gira o carro de acordo com a inclinacao
            self.rotateCar(window)

    def rotateCar(self, window):

        # gira a imagem
        if self.speed != 0:
            img_copy = pygame.transform.rotate(self.image, self.angle * -1)
            self.distances = drawAllLines(window,
                                          self.rect[0] - int(img_copy.get_width() / 2) + img_copy.get_width() / 2,
                                          self.rect[1] - int(img_copy.get_height() / 2) + + img_copy.get_height() / 2,
                                          self.angle * -1)

            if min(self.distances) <= img_copy.get_width() / 2:
                self.speed = 0
                self.play = False

            # Atualizar
            # window.blit(img_copy, (self.rect[0] - int(img_copy.get_width() / 2), self.rect[1] - int(img_copy.get_height() / 2)))


class Text:

    def __init__(self, size, text, font):
        pygame.font.init()
        self.font = pygame.font.Font("assets/font/" + font + ".ttf", size)
        self.render = self.font.render(text, True, (0, 0, 0))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def text_update(self, text):
        self.render = self.font.render(text, True, (0, 0, 0))
