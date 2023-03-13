import pygame
import math


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


pygame.init()

# Define as dimensões da tela
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Carrega imagem da pista e dos carros
background_surface = pygame.image.load("assets/pista3.png").convert()
image = pygame.image.load("assets/car_1.png")

# Define as coordenadas x e y, e as dimensões do retângulo
rect_x = 200
rect_y = 415

# Define a velocidade do carro e o angulo
speed = 1
angle = 0

clock = pygame.time.Clock()

# Loop principal
while True:

    # Eventos de saída
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            angle -= 3
        elif keys[pygame.K_d]:
            angle += 3

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    angle += 0.05
    angle %= 360

    # Converte o ângulo para radianos
    angle_rad = math.radians(angle)

    # Calcula a variação nas coordenadas x e y do retângulo
    delta_x = speed * math.cos(angle_rad)
    delta_y = speed * math.sin(angle_rad)

    # Atualiza as coordenadas x e y do retângulo
    rect_x += delta_x
    rect_y += delta_y

    # Background
    screen.blit(background_surface, (0, 0))

    # gira a imagem
    if speed != 0:
        img_copy = pygame.transform.rotate(image, angle * -1)
        distancias = drawAllLines(screen, rect_x - int(img_copy.get_width() / 2) + img_copy.get_width() / 2,
                                  rect_y - int(img_copy.get_height() / 2) + + img_copy.get_height() / 2, angle * -1)

        if min(distancias) <= img_copy.get_width() / 2:
            speed = 0

    # Atualizar
    screen.blit(img_copy, (rect_x - int(img_copy.get_width() / 2), rect_y - int(img_copy.get_height() / 2)))

    pygame.display.flip()
    clock.tick(60)