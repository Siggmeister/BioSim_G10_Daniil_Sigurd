# -*- coding: utf-8 -*-


import numpy as np
import random


class Animals:
    def __init__(self, loc, age=0):
        self.age = age
        self.loc = loc

    def aging(self):
        self.age += 1


class Herbivore(Animals):

    def __init__(self, island, parameters, loc, age=0, weight=None):
        super().__init__(loc, age)
        self.fitness = None
        self.parameters = parameters
        self.island = island

        if weight is None:
            self.weight = np.random.normal(self.parameters["w_birth"],
                                           self.parameters["sigma_birth"])

        else:
            self.weight = weight
            #Sett i Method for seg selv

        self.fitness_change()

    def fitness_change(self):
        phi_age_param = self.parameters["phi_age"]
        a_half_param = self.parameters["a_half"]
        phi_weight_param = self.parameters["phi_weight"]
        w_half_param = self.parameters["w_half"]

        if self.weight > 0:
            self.fitness = ((1 /
                            (1 + np.exp(phi_age_param *
                            (self.age - a_half_param)))) *
                            (1 / (1 + np.exp(-(phi_weight_param *
                            (self.weight - w_half_param))))))
        else: # Legg i variabler for å gjøre det finere
            self.fitness = 0

    def fodder_eaten(self):

        available_fodder = self.island.get_fodder_on_loc(self.loc)
        optimal_fodder = self.parameters["F"]
        fodder_eaten = 0

        if optimal_fodder <= available_fodder:
            fodder_eaten = optimal_fodder

        elif available_fodder > 0 and available_fodder < optimal_fodder:
            fodder_eaten = available_fodder

        elif available_fodder == 0:
            fodder_eaten = 0
            #Raise Value Error hvis negativ

        self.island.herb_eats_fodder(self.loc, fodder_eaten)

        return fodder_eaten

    def weight_gain(self, consumption):
        self.weight += consumption * self.parameters["beta"]

    def feed(self):
        consumed_fodder = self.fodder_eaten()
        self.weight_gain(consumed_fodder)
        self.fitness_change()

    def count_all_herb_in_current_loc(self, herb_pop_list):
        counter = 0
        for herb in herb_pop_list:
            if herb.loc == self.loc:
                counter += 1
        return counter

    def can_birth_occur(self, herb_pop_list):
        num_prob = min(1, self.parameters["gamma"] * self.fitness *
                       (self.count_all_herb_in_current_loc(herb_pop_list) - 1))

        weight_prob = (self.parameters["zeta"] *
                       (self.parameters["w_birth"] + self.parameters[
                           "sigma_birth"]))

        if num_prob == 0 or weight_prob > self.weight:
            return False

        if random.random() <= num_prob:
            return True
        else:
            return False

    def birth(self, herb_pop_list):
        if self.can_birth_occur(herb_pop_list):
            baby_herb = Herbivore(self.island, self.parameters, self.loc)

            weight_loss_by_birth = baby_herb.weight * self.parameters["xi"]

            if weight_loss_by_birth < self.weight:
                herb_pop_list.append(baby_herb)

    def annual_weight_loss(self):
        self.weight -= self.parameters["eta"] * self.weight

    def death(self):

        death_prob = self.parameters["omega"] * (1 - self.fitness)

        if self.fitness == 0:
            return True

        elif random.random() <= death_prob:
            return True

        else:
            return False
