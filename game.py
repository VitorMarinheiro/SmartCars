from operator import attrgetter
import random
import pygame
import numpy as np
import configparser
from ia import LayerDense, ActivationReLu
from obj import Obj, Car
config = configparser.ConfigParser()
config.read('config.properties')


class Game:

    def __init__(self):

        self.window = 0
        self.tam_population = 5
        self.generation = 0
        self.best_score = 0
        self.score = 0
        self.start_game([])
        self.score_value = 0
        self.playing = True
        self.ticks = 0
        self.all_dead = False
        self.count_dead_time = 0
        self.re_lu = ActivationReLu()

    def draw(self, window):
        self.window = window
        self.background.draw(window)
        self.car_group.draw(window)

    def validate_population_alive(self):
        for car in self.population:
            if car.play:
                return True
        return False

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
                    if output[0] > 1:
                        car.speed += 0.2
                        if car.speed > 5:
                            car.speed = 5
                        print('Acelerando')
                    if output[1] > 1:
                        car.speed -= 0.2
                        print('Freando')
                        if car.speed < 1:
                            car.speed = 1
                    if output[2] > 1:
                        print('Esquerda')
                        car.angle += 0.1
                    if output[3] > 1:
                        print('Direita')
                        car.angle -= 0.1


                    # Seta valor de score
                    for car in self.population:
                        if car.play:
                            if car.score > self.score_value:
                                self.score_value = car.score
                                if self.score_value > self.best_score:
                                    self.best_score = self.score_value
        else:

            # Delay para mostrar animacao de ultimo morto
            self.all_dead = True
            self.count_dead_time += 1

            # Reseta game apos delay
            if self.count_dead_time > 10:
                max_attr = max(self.population, key=attrgetter('fitness'))
                self.population[0] = max_attr
                self.start_game(self.population)
                self.ticks = 0
                self.score_value = 0
                self.count_dead_time = 0
                self.all_dead = False

        # Update sprites
        # self.car_group.update(window)

        # Captura eventos de clique
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def start_game(self, listOfCars):
        self.generation += 1

        self.background = pygame.sprite.Group()
        self.car_group = pygame.sprite.Group()

        self.bg = Obj("assets/pista4.png", 0, 0, self.background)

        # Reseta a populacao
        new_population = []

        for index_population in range(0, self.tam_population):
            new_car = Car("assets/car_1.png", self.car_group)
            new_car.dense1 = LayerDense(7, 6)
            new_car.dense2 = LayerDense(6, 4)
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
