# -*- coding: utf-8 -*-


import numpy as np
import random



class Animals:

    animal_parameters = {"Herbivore": {"w_birth": 8.0,
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
                                            "F": 10.0},

                              "Carnivore": {"w_birth": 6.0,
                                            "sigma_birth": 1.0,
                                            "beta": 0.75,
                                            "eta": 0.0125,
                                            "a_half": 60.0,
                                            "phi_age": 0.4,
                                            "w_half": 4.0,
                                            "phi_weight": 0.4,
                                            "mu": 0.4,
                                            "lambda": 1.0,
                                            "gamma": 0.8,
                                            "zeta": 3.5,
                                            "xi": 1.1,
                                            "omega": 0.9,
                                            "F": 50.0,
                                            "DeltaPhiMax": 10.0}}

    def __init__(self, island, loc, age=0):
        self.age = age
        self.loc = loc
        self.island = island
        self.island.add_pop_on_loc(self.loc, self)
        self.fitness = None


    def aging(self):
        self.age += 1

    def get_loc(self):
        return self.loc

    def get_fitness(self):
        return self.fitness

    @classmethod
    def param_changer(cls, species, new_params):
        for key in new_params:
            Animals.animal_parameters[species][key] = new_params[key]


class Herbivore(Animals):

    def __init__(self, island, loc, age=0, weight=None):
        super().__init__(island, loc, age)

        if weight is None:
            self.weight = self._set_weight()

        else:
            self.weight = weight

        self.fitness_change()

    @staticmethod
    def _set_weight():
        w_birth = Animals.animal_parameters["Herbivore"]["w_birth"]
        sigma_birth = Animals.animal_parameters["Herbivore"]["sigma_birth"]

        return np.random.normal(w_birth, sigma_birth)

    def fitness_change(self):
        phi_age = Animals.animal_parameters["Herbivore"]["phi_age"]
        a_half = Animals.animal_parameters["Herbivore"]["a_half"]
        phi_weight = Animals.animal_parameters["Herbivore"]["phi_weight"]
        w_half = Animals.animal_parameters["Herbivore"]["w_half"]

        if self.weight > 0:
            self.fitness = ((1 /
                            (1 + np.exp(phi_age *
                            (self.age - a_half)))) *
                            (1 / (1 + np.exp(-(phi_weight *
                            (self.weight - w_half))))))
        else:
            self.fitness = 0

    def fodder_eaten(self):

        available_fodder = self.island.get_fodder_on_loc(self.loc)

        optimal_fodder = Animals.animal_parameters["Herbivore"]["F"]


        if optimal_fodder <= available_fodder:
            fodder_eaten = optimal_fodder

        elif available_fodder > 0 and available_fodder < optimal_fodder:
            fodder_eaten = available_fodder

        elif available_fodder == 0:
            fodder_eaten = 0
            
        else:
            raise ValueError

        return fodder_eaten

    def weight_gain(self, consumption):
        beta = Animals.animal_parameters["Herbivore"]["beta"]

        self.weight += consumption * beta

    def feed(self):
        consumed_fodder = self.fodder_eaten()
        self.island.herb_eats_fodder_on_loc(self.loc, consumed_fodder)
        self.weight_gain(consumed_fodder)
        self.fitness_change()

    def can_birth_occur(self):
        gamma = Animals.animal_parameters["Herbivore"]["gamma"]
        zeta = Animals.animal_parameters["Herbivore"]["zeta"]
        w_birth = Animals.animal_parameters["Herbivore"]["w_birth"]
        sigma_birth = Animals.animal_parameters["Herbivore"]["sigma_birth"]

        num_prob = min(1, gamma * self.fitness *
                       (self.island.get_herb_pop_on_loc(self.loc) - 1))

        weight_prob = (zeta * (w_birth + sigma_birth))

        if num_prob == 0 or weight_prob > self.weight:
            return False

        if random.random() <= num_prob:
            return True
        else:
            return False

    def birth(self, herb_pop_list):
        xi = Animals.animal_parameters["Herbivore"]["xi"]

        if self.can_birth_occur():
            baby_herb = Herbivore(self.island, self.loc)

            weight_loss_by_birth = baby_herb.weight * xi

            if weight_loss_by_birth < self.weight:
                herb_pop_list.append(baby_herb)
                self.island.add_pop_on_loc(self.loc, baby_herb)

    def annual_weight_loss(self):
        eta = Animals.animal_parameters["Herbivore"]["eta"]

        self.weight -= eta * self.weight

    def death(self):
        omega = Animals.animal_parameters["Herbivore"]["omega"]
        death_prob = omega * (1 - self.fitness)

        if self.fitness == 0:
            return True

        elif random.random() <= death_prob:
            return True

        else:
            return False

class Carnivore(Animals):

    def __init__(self, island, loc, age=0, weight=None):
        pass
