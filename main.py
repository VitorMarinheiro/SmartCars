import pygame
import configparser
from game import Game
from utils import capturar_matriz_de_pixels, wavefront, get_matriz_pixels

config = configparser.ConfigParser()
config.read('config.properties')


class Main:

    def __init__(self):
        """Inicializador das variáveis necessárias"""

        # captura matriz de pixel e custo da pista escolhida
        capturar_matriz_de_pixels()
        wavefront()

        # inicializa o pygame
        self.window = pygame.display.set_mode([700, 700])
        pygame.display.set_caption("Smart Cars")
        pygame.display.set_icon(
            pygame.transform.scale(pygame.image.load("assets/car_1.png"), (555, 555))
        )

        self.loop = True
        self.fps = pygame.time.Clock()
        self.game = Game()

    def events(self):
        """Captura todos os eventos ocorridos no pygame, como clicks, botões e afins"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False

    def draw(self):
        """Insere na janela do pygame todos os elementos necessários abaixo do self.game"""
        self.game.draw(self.window)
        self.game.update(self.window)

    def update(self):
        """Realiza o update do pygame de acordo com o fps definido"""
        while self.loop:
            self.fps.tick(int(config.get('pygame', 'fps')))
            self.events()
            self.draw()
            pygame.display.update()


Main().update()