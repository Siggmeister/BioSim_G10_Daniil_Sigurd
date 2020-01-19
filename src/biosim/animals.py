# -*- coding: utf-8 -*-


import numpy as np
import random



class Animals:
    parameters = None

    def __init__(self, island, loc, age=0, weight=None):
        self.age = age
        self.loc = loc
        self.island = island
        self.island.add_pop_on_loc(self.loc, self)
        self.fitness = None

        if weight is None:
            self.weight = self.set_birth_weight()

        else:
            self.weight = weight

        self.fitness_change()
        #Check sepcies NameError

    def aging(self):
        self.age += 1

    def get_loc(self):
        return self.loc

    def get_fitness(self):
        return self.fitness

    @classmethod
    def param_changer(cls, new_params):
         cls.parameters.update(new_params)

    def set_birth_weight(self):
        w_birth = self.parameters["w_birth"]
        sigma_birth = self.parameters["sigma_birth"]

        return np.random.normal(w_birth, sigma_birth)

    def fitness_change(self):
        phi_age = self.parameters["phi_age"]
        a_half = self.parameters["a_half"]
        phi_weight = self.parameters["phi_weight"]
        w_half = self.parameters["w_half"]

        if self.weight > 0:
            self.fitness = ((1 /
                            (1 + np.exp(phi_age *
                            (self.age - a_half)))) *
                            (1 / (1 + np.exp(-(phi_weight *
                            (self.weight - w_half))))))
        else:
            self.fitness = 0

    def weight_gain(self, consumption):
        beta = self.parameters["beta"]

        self.weight += consumption * beta
        self.fitness_change()

    def can_birth_occur(self):
        gamma = self.parameters["gamma"]
        zeta = self.parameters["zeta"]
        w_birth = self.parameters["w_birth"]
        sigma_birth = self.parameters["sigma_birth"]

        num_prob = min(1, gamma * self.fitness *
                           (self.get_num_same_species(self.loc) - 1))

        weight_prob = (zeta * (w_birth + sigma_birth))

        if num_prob == 0 or weight_prob > self.weight:
            return False

        if random.random() <= num_prob:
            return True
        else:
            return False

    def birth(self):
        xi = self.parameters["xi"]

        if self.can_birth_occur():
            if self.__class__.__name__ == "Herbivore":
                baby_animal = Herbivore(self.island, self.loc)
            elif self.__class__.__name__ == "Carnivore":
                baby_animal = Carnivore(self.island, self.loc)

            weight_loss_by_birth = baby_animal.weight * xi

            if weight_loss_by_birth >= self.weight:
                self.island.remove_pop_on_loc(self.loc, baby_animal)

    def annual_weight_loss(self):
        eta = self.parameters["eta"]

        self.weight -= eta * self.weight
        self.fitness_change()

    def death(self):
        omega = self.parameters["omega"]
        death_prob = omega * (1 - self.fitness)

        if self.fitness == 0:
            return True

        elif random.random() <= death_prob: #SJEKK ALLE SANNSYNLIGHETER, om <= blir riktig
            return True

        else:
            return False

    def will_move(self):
        mu = self.parameters["mu"]

        if random.random() <= mu * self.fitness:
            return True
        else:
            return False

    def get_relevant_fodder(self, loc):
        if self.__class__.__name__ == "Herbivore":
            return self.island.get_fodder_on_loc(loc)
        elif self.__class__.__name__ == "Carnivore":
            return self.island.get_total_herb_weight_on_loc(loc)

    def get_num_same_species(self, loc):
        if self.__class__.__name__ == "Herbivore":
            return self.island.get_num_herb_on_loc(loc)
        elif self.__class__.__name__ == "Carnivore":
            return self.island.get_num_carn_on_loc(loc)

    def relative_abundance(self, loc):
        F = self.parameters["F"]
        num_same_species = self.get_num_same_species(loc)
        relevant_fodder = self.get_relevant_fodder(loc)
        relative_abundance = relevant_fodder/((num_same_species + 1) * F)
        return relative_abundance

    def propensity(self, loc):
        lambda_ = self.parameters["lambda"]
        relative_abundance = self.relative_abundance(loc)
        cell_type = self.island.get_cell_type(loc)

        if cell_type == "Mountain" or cell_type == "Ocean":
            return 0
        else:
            return np.exp(lambda_ * relative_abundance)

    def get_potential_coordinates(self):
        loc_1 = (self.loc[0] + 1, self.loc[1])
        loc_2 = (self.loc[0] - 1, self.loc[1])
        loc_3 = (self.loc[0], self.loc[1] + 1)
        loc_4 = (self.loc[0], self.loc[1] - 1)
        loc_list = [loc_1, loc_2, loc_3, loc_4]
        return loc_list

    def total_propensity(self, loc_list):
        total_propensity = 0
        for loc in loc_list:
            total_propensity += self.propensity(loc)
        return total_propensity

    def probabilities(self, loc_list):
        probability_list = []
        total_propensity = self.total_propensity(loc_list)
        if total_propensity == 0:
            return None
        for loc in loc_list:
            propensity = self.propensity(loc)
            probability = propensity/total_propensity
            probability_list.append(probability)
        return probability_list

    def destination(self, loc_list):
        prob_list = self.probabilities(loc_list)
        if prob_list is None:
            return None
        else:
            destination_index = np.random.choice(range(len(loc_list)), p=prob_list)
            destination = loc_list[destination_index]
            return destination

    def migrate(self):
        if self.will_move():
            loc_list = self.get_potential_coordinates()
            destination = self.destination(loc_list)
            if destination is None:
                pass
            else:
                self.island.remove_pop_on_loc(self.loc, self)
                self.island.add_pop_on_loc(destination, self)
                self.loc = destination


class Herbivore(Animals):
    parameters = {"w_birth": 8.0,
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

    def __init__(self, island, loc, age=0, weight=None):
        super().__init__(island, loc, age, weight)

    def eaten(self):
        self.island.remove_pop_on_loc(self.loc, self)

    def fodder_eaten(self):

        available_fodder = self.island.get_fodder_on_loc(self.loc)

        optimal_fodder = self.parameters["F"]

        if optimal_fodder <= available_fodder:
            fodder_eaten = optimal_fodder

        elif 0 < available_fodder < optimal_fodder:
            fodder_eaten = available_fodder

        elif available_fodder == 0:
            fodder_eaten = 0

        else:
            raise ValueError

        return fodder_eaten


    def feed(self):
        consumed_fodder = self.fodder_eaten()
        self.island.herb_eats_fodder_on_loc(self.loc, consumed_fodder)
        self.weight_gain(consumed_fodder)


class Carnivore(Animals):

    parameters = {"w_birth": 6.0,
                                            "sigma_birth": 1.0,
                                            "beta": 0.75,
                                            "eta": 0.125,
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
                                            "DeltaPhiMax": 10.0}

    def __init__(self, island, loc, age=0, weight=None):
        super().__init__(island, loc, age, weight)

    def kill_herb(self, herb):
        DeltaPhiMax = self.parameters["DeltaPhiMax"]
        herb_fitness = herb.get_fitness()
        fitness_diff = self.fitness - herb_fitness
        if self.fitness <= herb_fitness:
            kill_prob = 0
        elif 0 < fitness_diff < DeltaPhiMax:
            kill_prob = (self.fitness - herb_fitness)/DeltaPhiMax
        else:
            kill_prob = 1

        if random.random() <= kill_prob:
            return True
        else:
            return False

    def feed(self):
        herbs_in_loc = self.island.get_herb_list_on_loc(self.loc)
        herbs_in_loc.sort(key=lambda herb: herb.fitness) # Tries to kill the herbivore with the lowest fitness first
        desired_weight = self.parameters["F"]
        killed_weight = 0
        index = 0

        while killed_weight < desired_weight and index < len(herbs_in_loc):
            herb = herbs_in_loc[index]
            if self.kill_herb(herb):
                last_kill = herb.weight
                appetite_weight = self.appetite_checker(killed_weight, desired_weight, last_kill)
                killed_weight += last_kill
                self.weight_gain(appetite_weight)
                herb.eaten()
            index += 1

    @staticmethod
    def appetite_checker(eaten_weight, desired_weight, kill_weight):
        if eaten_weight + kill_weight > desired_weight:
            appetite_weight = desired_weight - eaten_weight
            return appetite_weight
        else:
            return kill_weight
