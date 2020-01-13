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
                                         "F": 10.0}}

    def __init__(self, loc, age=0):
        self.age = age
        self.loc = loc

    def aging(self):
        self.age += 1

    @classmethod
    def param_changer(cls, species, new_params):
        for key in new_params:
            Animals.animal_parameters[species][key] = new_params[key]


class Herbivore(Animals):

    def __init__(self, island, loc, age=0, weight=None):
        super().__init__(loc, age)
        self.fitness = None
        self.parameters = None
        self.island = island
        w_birth_param = Animals.animal_parameters["Herbivore"]["w_birth"]
        sigma_birth_param = Animals.animal_parameters["Herbivore"]["sigma_birth"]

        if weight is None:
            self.weight = np.random.normal(w_birth_param,
                                           sigma_birth_param)

        else:
            self.weight = weight
            #Sett i Method for seg selv

        self.fitness_change()

    def fitness_change(self):
        phi_age_param = Animals.animal_parameters["Herbivore"]["phi_age"]
        a_half_param = Animals.animal_parameters["Herbivore"]["a_half"]
        phi_weight_param = Animals.animal_parameters["Herbivore"]["phi_weight"]
        w_half_param = Animals.animal_parameters["Herbivore"]["w_half"]

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
        optimal_fodder = Animals.animal_parameters["Herbivore"]["F"]
        fodder_eaten = 0

        if optimal_fodder <= available_fodder:
            fodder_eaten = optimal_fodder

        elif available_fodder > 0 and available_fodder < optimal_fodder:
            fodder_eaten = available_fodder

        elif available_fodder == 0:
            fodder_eaten = 0
            
        else:
            raise ValueError

        self.island.herb_eats_fodder(self.loc, fodder_eaten)

        return fodder_eaten

    def weight_gain(self, consumption):
        beta_param = Animals.animal_parameters["Herbivore"]["beta"]

        self.weight += consumption * beta_param

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
        gamma_param = Animals.animal_parameters["Herbivore"]["gamma"]
        zeta_param = Animals.animal_parameters["Herbivore"]["zeta"]
        w_birth_param = Animals.animal_parameters["Herbivore"]["w_birth"]
        sigma_birth_param = Animals.animal_parameters["Herbivore"]["sigma_birth"]
        
        num_prob = min(1, gamma_param * self.fitness *
                       (self.count_all_herb_in_current_loc(herb_pop_list) - 1))

        weight_prob = (zeta_param *
                       (w_birth_param + sigma_birth_param))

        if num_prob == 0 or weight_prob > self.weight:
            return False

        if random.random() <= num_prob:
            return True
        else:
            return False

    def birth(self, herb_pop_list):
        xi_param = Animals.animal_parameters["Herbivore"]["xi"]

        if self.can_birth_occur(herb_pop_list):
            baby_herb = Herbivore(self.island, self.loc)

            weight_loss_by_birth = baby_herb.weight * xi_param

            if weight_loss_by_birth < self.weight:
                herb_pop_list.append(baby_herb)

    def annual_weight_loss(self):
        eta_param = Animals.animal_parameters["Herbivore"]["eta"]

        self.weight -= eta_param * self.weight

    def death(self):
        omega_param = Animals.animal_parameters["Herbivore"]["omega"]
        death_prob = omega_param * (1 - self.fitness)

        if self.fitness == 0:
            return True

        elif random.random() <= death_prob:
            return True

        else:
            return False
