from collections import deque
import numpy as np
import pygame
import matplotlib.pyplot as plt

GREY = 4285756275
start = (315, 415)
goal = (215, 415)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700


# Busca do custo de todos os pixels do mapa utilizando o algoritmo wavefront
def wavefront(start, goal, matrix):
    # Crie uma matriz de custos com todos os elementos iguais a zero
    cost_matrix = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    # Defina o valor do ponto de partida na matriz de custos como 1 e adicione-o à fila de busca
    cost_matrix[start[0]][start[1]] = 1
    queue = deque([start])

    # Loop enquanto a fila de busca não estiver vazia
    while queue:
        # Retire o primeiro elemento da fila de busca
        current = queue.popleft()

        # Se o elemento atual for o objetivo, interrompa o loop
        # Devemos retirar essa linha para que o wavefront busque todos os caminhos possiveis
        # if current == goal:
        #     break

        # Para cada vizinho do elemento atual na matriz inicial
        for neighbor in ((current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1),
                         (current[0], current[1] - 1)):
            row, col = neighbor

            # Verifique se o vizinho não é uma parede e se o custo do vizinho na matriz de custos ainda é zero
            if 0 <= row < SCREEN_WIDTH and 0 <= col < SCREEN_HEIGHT and matrix[row][col] == GREY and cost_matrix[row][
                col] == 0:
                # Defina o custo do vizinho como o custo do elemento atual mais 1 e adicione o vizinho à fila de busca
                cost_matrix[row][col] = cost_matrix[current[0]][current[1]] + 1
                queue.append(neighbor)

    # Salva essa matriz no arquivo de texto
    np.savetxt('outputs/cost.txt', cost_matrix, fmt='%d')


# Transforma os custos em uma cor no formato RGB
def get_rgb_color(value):
    """
    Retorna uma cor RGB de acordo com o valor de entrada.

    Parâmetros:
        value (int): valor entre 1 e 4000.

    Retorno:
        tuple: uma tupla contendo os valores das componentes Red, Green e Blue.
    """

    if value != 0:
        # Limita o valor de entrada entre 1 e 4000
        value = max(1, min(3000, value))

        # Calcula os valores das componentes Red, Green e Blue
        red = int(value / 20) + 55
        green = int(value / 40) + 52
        blue = int(value / 80) + 56

        # Limita os valores entre 0 e 255
        red = min(255, max(0, red))
        green = min(255, max(0, green))
        blue = min(255, max(0, blue))

    else:
        return (0, 0, 0)

    # Retorna uma tupla contendo as componentes Red, Green e Blue
    return (red, green, blue)


# Desenha o mapa de calor do wavefront e mostra os custos de acordo com a posicao do mouse
def desenhar_custos():
    grid = np.loadtxt('outputs/cost.txt', dtype=int)

    # Inicializa o Pygame
    pygame.init()

    # Cria a janela
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Pinta cada pixel da janela com base nos valores da matriz
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # Calcula as coordenadas do pixel na tela
            x = col * 1
            y = row * 1
            # Obtém a cor do pixel a partir da matriz
            color = get_rgb_color(grid[row][col])
            pygame.draw.rect(window, color, (y, x, 1, 1))

    # Mantém a janela aberta até que o usuário a feche
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        mousepos = pygame.mouse.get_pos()
        print(grid[mousepos])

        # Atualiza a tela
        pygame.display.flip()


# Captura as cores dos pixels da tela e salva em um arquivo texto padrao
def capturar_matriz_de_pixels():
    # Abre a imagem na janela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_surface = pygame.image.load("assets/pista4.png").convert()
    screen.blit(background_surface, (0, 0))

    # Captura a matriz 2d de cores
    pixels = pygame.surfarray.pixels2d(screen)

    # Salva essa matriz no arquivo de texto
    np.savetxt('outputs/pixels.txt', pixels, fmt='%d')


# Retorna o custo atual da posicao
def get_custo_posicao(pos):
    # Carrega a matriz com os pixels de acordo com a cor
    matrix = np.loadtxt('outputs/cost.txt', dtype=int)

    return matrix[pos]


def get_matriz_pixels():
    return np.loadtxt('outputs/pixels.txt', dtype=int)


def get_matriz_custo():
    return np.loadtxt('outputs/cost.txt', dtype=int)


# capturar_matriz_de_pixels()
# wavefront(start, goal, get_matriz_pixels())
# desenhar_custos()
# #
