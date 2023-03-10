from PIL import Image
import numpy as np
import pygame
from Car import Car

class MyGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)


background_image = Image.open("assets/pista3.png")

# Definir a largura e a altura da janela
LARGURA = 700
ALTURA = 700

# Gerar uma matriz 2D com 1 elemento para cada pixel da imagem
matriz = np.zeros((ALTURA, LARGURA, 3), dtype=np.uint8)

for x in range(LARGURA):
    for y in range(ALTURA):
        r, g, b, o = background_image.getpixel((x, y))
        matriz[x][y] = (r, g, b)

# Criar a janela
pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
background_surface = pygame.image.load("assets/pista3.png").convert()

# Definir o tamanho dos pixels
tamanho_pixel = int(LARGURA / matriz.shape[0])

car_group = pygame.sprite.Group()
MyGroup.add(Car(janela, car_group))

# Loop principal
while True:

    # Eventos de saída
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            print('Seta para cima pressionada')
        elif keys[pygame.K_s]:
            print('Seta para baixo pressionada')
        elif keys[pygame.K_a]:
            print('Seta para a esquerda pressionada')
            for car in car_group:
                car.rotate(-10)
        elif keys[pygame.K_d]:
            print('Seta para a direita pressionada')
            for car in car_group:
                car.rotate(-10)

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # # Loop para desenhar os pixels
    # for i in range(matriz.shape[0]):
    #     for j in range(matriz.shape[1]):
    #
            # # Definir a cor do pixel
            # if np.any(matriz[i, j] == np.array([115, 115, 115])):
            #     pygame.draw.rect(janela, matriz[i, j], (i * tamanho_pixel, j * tamanho_pixel, tamanho_pixel, tamanho_pixel))

    # Desenha o Background
    janela.blit(background_surface, (0, 0))

    MyGroup.update(self)
    MyGroup.draw()
    # car_group.draw(janela)

    # Atualizar a janela
    pygame.display.update()

