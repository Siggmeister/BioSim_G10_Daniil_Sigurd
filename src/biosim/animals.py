# -*- coding: utf-8 -*-


import numpy as np
import random


class Animals:
    def __init__(self, loc, age=0):
        self.age = age
        self.loc = loc

    def age(self):
        self.age += 1


class Herbivore(Animals):
    param_dict = {"w_birth": 8.0,
                  "sigma_birth": 1.5,
                  "beta": 0.9,
                  "eta": 0.05,
                  "a_half": 40.0,
                  "phi_age": 0.2,
                  "w_half": 10.0,
                  "phi_weight": 0.1,
                  "mu": 0.25,
                  "lambda": 1.0,
                  "gamma": 0.2,
                  "zeta": 3.5,
                  "xi": 1.2,
                  "omega": 0.4,
                  "F": 10.0}

    def __init__(self, loc, age=0, parameters=None, weight=None):
        super().__init__(age, loc)

        if parameters is None:
            parameters = Herbivore.param_dict
        # self.parameters = parameters

        for key in parameters:
            Herbivore.param_dict[key] = parameters[key]
            self.parameters = Herbivore.param_dict

        if weight is None:
            self.weight = np.random.normal(self.parameters["w_birth"],
                                           self.parameters["sigma_birth"])

        else:
            self.weight = weight

        self.fitness_change()

    def fitness_change(self):
        if self.weight > 0:
            self.fitness = (((1) / (1 + np.exp(self.parameters["phi_age"] *
                                               (self.age - self.parameters[
                                                   "a_half"])))) *
                            ((1) / (1 + np.exp(-self.parameters["phi_weight"] *
                                               (self.weight - self.parameters[
                                                   "w_half"])))))
        else:
            self.fitness = 0

    def param_changer(self, parameters):

        for key in parameters:
            Herbivore.param_dict = parameters[key]

        return Herbivore.param_dict

    def fodder_eaten(self, island_dict):

        available_fodder = island_dict[self.loc]["Fodder"]
        optimal_fodder = self.parameters["F"]
        fodder_eaten = 0

        if optimal_fodder <= available_fodder:
            fodder_eaten = optimal_fodder

        elif available_fodder > 0 and available_fodder < optimal_fodder:
            fodder_eaten = available_fodder

        elif available_fodder == 0:
            fodder_eaten = 0

        island_dict[self.loc]["Fodder"] -= fodder_eaten

        return fodder_eaten

    def weight_gain(self, consumption):
        self.weight += consumption * self.parameters["beta"]

    def feed(self, island_dict):
        consumed_fodder = self.fodder_eaten(island_dict)
        self.weight_gain(consumed_fodder)
        self.fitness_change()

    def can_birth_occur(self, island_dict):
        num_prob = min(1, self.parameters["gamma"] * self.fitness *
                       (island_dict[self.loc]["Herb_pop"] - 1))
        # Sjekk dictionary herb-ammount

        weight_prob = (self.parameters["zeta"] *
                       (self.parameters["w_birth"] + self.parameters[
                           "sigma_birth"]))

        if num_prob == 0 or weight_prob > self.weight:
            return False

        if random.random() <= num_prob:
            return True
        else:
            return False

    def birth(self, island_dict):
        if self.can_birth_occur(island_dict):
            baby_herb = Herbivore(self.loc)

            weight_loss_by_birth = baby_herb.weight * self.paramterers["xi"]

            if weight_loss_by_birth < self.weight:
                # Append i liste med alle herbivores
                pass

    def death(self):

        death_prob = self.parameters["omega"] * (1 - self.fitness)

        if self.fitness == 0:
            return True

        elif random.random() <= death_prob:
            return True

        else:
            return False