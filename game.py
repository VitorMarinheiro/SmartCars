from operator import attrgetter
import random
import pygame
import numpy as np
import configparser
from ia import LayerDense, ActivationReLu
from obj import Obj, Car, Text, Button, Chart
from utils import get_matriz_pixels, get_matriz_custo

config = configparser.ConfigParser()
config.read('config.properties')

msgGeneration = "Generation: "
msgPopulation = "Population: "
msgRemCars = "Remaining Cars: "
msgLastScore = "Last Score: "
msgBestScoreHist = "Best Score: "

biggestScorePossible = 2420


class Game:

    def __init__(self):

        self.window = 0
        self.tam_population = int(config.get('geracoes', 'population'))
        self.generation = 0
        self.best_score = 0
        self.score = 0
        self.start_game([])
        self.playing = True
        self.ticks = 0
        self.all_dead = False
        self.count_dead_time = 0
        self.re_lu = ActivationReLu()
        self.graph = Chart(50, 580, 100, 400)
        self.hist_y = []

    def draw(self, window):
        self.window = window
        self.background.draw(window)
        self.button_grades.draw(window)
        self.graph.draw(window)
        for text in self.texts:
            text.draw(window)
        # self.car_group.draw(window)  # Nao eh necessario desenhar o grupo, pois o carro esta sendo desenhado no rotate

    def validate_population_alive(self):
        for car in self.population:
            if car.play:
                return True
        return False

    def get_score_percent(self, score):
        return str(int((score / biggestScorePossible) * 100)) + '%'

    def update(self, window):
        vivos = 0
        if self.validate_population_alive():
            for car in self.population:
                if car.play:
                    vivos += 1
                    car.update(self.window)
                    car.dense1.forward(np.array(car.distances))
                    car.dense2.forward(self.re_lu.forward(car.dense1.output))
                    output = self.re_lu.forward(car.dense2.output)
                    output = output[0].tolist()

                    # Aplica resultados da RN
                    if output[0] > 0:
                        car.speed += 0.2
                        if car.speed > 5:
                            car.speed = 5
                    if output[1] > 0:
                        car.speed -= 0.2
                        if car.speed < 1:
                            car.speed = 1
                    if output[2] > 0:
                        # print('Esquerda')
                        car.angle += 1.5 * car.speed
                    if output[3] > 0:
                        # print('Direita')
                        car.angle -= 1.5 * car.speed

            # Atualiza texto de carros vivos
            self.texts[2].text_update(msgRemCars + str(vivos))

        else:

            # Delay para mostrar animacao de ultimo morto
            self.all_dead = True
            self.count_dead_time += 1

            # Reseta game apos delay
            if self.count_dead_time >= 1:

                # Seta valor de score
                max_attr = max(self.population, key=attrgetter('fitness'))
                self.score = max_attr.fitness
                self.hist_y.append(self.score + 1)
                self.population[0] = max_attr
                self.ticks = 0
                self.count_dead_time = 0
                self.all_dead = False
                self.graph.update(self.generation, self.hist_y)
                print(self.generation, ' --------------- ', self.score, ' ---------------')

                # Atualiza o melhor score historico
                if self.score > self.best_score:
                    self.best_score = self.score

                # Inicia um novo game
                self.start_game(self.population)

        # Update sprites

        # Captura eventos de clique
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            self.button_grades.handle_event(event)

    def start_game(self, listOfCars):
        self.generation += 1

        self.background = pygame.sprite.Group()
        self.car_group = pygame.sprite.Group()
        self.texts = []
        self.texts.append(Text(15, msgGeneration + str(self.generation), "OpenSans-Regular", 60, 480))
        self.texts.append(Text(15, msgPopulation + str(self.tam_population), "OpenSans-Regular", 60, 500))
        self.texts.append(Text(15, msgRemCars + str(self.tam_population), "OpenSans-Regular", 60, 520))
        self.texts.append(Text(15, msgLastScore + str(self.get_score_percent(self.score)), "OpenSans-Regular", 60, 540))
        self.texts.append(
            Text(15, msgBestScoreHist + str(self.get_score_percent(self.best_score)), "OpenSans-Regular", 60, 560))
        self.button_grades = Button(250, 480, 200, 80, "GRADES")
        self.bg = Obj("assets/pista4_separada.png", 0, 0, self.background)

        # Reseta a populacao
        new_population = []

        # Captura os valores do mapa
        matrizPixels = get_matriz_pixels()
        matrizCusto = get_matriz_custo()

        for index_population in range(0, self.tam_population):
            new_car = Car("assets/car_1.png", matrizPixels, matrizCusto, self.car_group)
            new_car.dense1 = LayerDense(7, 8)
            new_car.dense2 = LayerDense(8, 4)
            if len(listOfCars) > 0:
                new_car.dense1.weights = listOfCars[0].dense1.weights.copy()
                new_car.dense2.weights = listOfCars[0].dense2.weights.copy()
            new_population.append(new_car)

        # Aplica mutacao
        for index in range(0, self.tam_population):
            if (len(listOfCars) > 0) and (index > 0):
                new_population[index].dense1.random_weights()
                new_population[index].dense2.random_weights()

        self.population = new_population[:]
