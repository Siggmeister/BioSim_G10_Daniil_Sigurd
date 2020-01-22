# -*- coding: utf-8 -*-


import numpy as np
import random
from math import exp
from island import *

class Animals:
    """SUMMARY

    :param island: An instance of the :class:'src.biosim.island.Island'
    with data and methods, containing info about the geography.
    :type island: class:'src.biosim.island.Island'
    :param loc: Indicates the coordinates of the animal
    :type loc: tuple
    :param age: Indicates the age of the animal, defaults to 0
    :type age: int, optional
    :param weight: Indicates the weight of the animal, defaults to None
    :type weight: float, optional
    """
    parameters = None

    def __init__(self, island, loc, age=0, weight=None):
        """Constructor method.
        """
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
        """Adds a year to the self.age variable.
        """
        self.age += 1
        self.fitness_change()

    def get_loc(self):
        """Returns the coordinates of the animal.

        :return: A tuple with x and y coordinates.
        :rtype: tuple
        """
        return self.loc

    def get_fitness(self):
        """Returns the fitness of the animal.

        :return: Fitness of the animal
        :rtype: float
        """
        return self.fitness

    @classmethod
    def param_changer(cls, new_params):
        """Changes the parameters of either Herbivore or Carnivore class.

        :param new_params: Dictionary containing the changed parameter
        :type new_params: dict
        """
        params_non_negative = ["w_birth", "sigma_birth", "gamma", "xi", "F"]
        for key in new_params:
            if key not in cls.parameters:
                raise ValueError("Can not change parameter "
                                 "'{0}' since the parameter does "
                                 "not exist in default-list".format(key))

            if key in params_non_negative and new_params[key] < 0:
                raise ValueError("Parameter {0} must be a nonnegative value."
                                 .format(key))

        cls.parameters.update(new_params)



    def set_birth_weight(self):
        """Sets the animals birth-weight to a float
        between the two given parameters.

        :return: A float between w_birth and sigma_birth
        :rtype: float
        """
        w_birth = self.parameters["w_birth"]
        sigma_birth = self.parameters["sigma_birth"]

        return np.random.normal(w_birth, sigma_birth)

    def fitness_change(self):
        """Changes the fitness according to a formula using given parameters.
        """
        phi_age = self.parameters["phi_age"]
        a_half = self.parameters["a_half"]
        phi_weight = self.parameters["phi_weight"]
        w_half = self.parameters["w_half"]

        if self.weight > 0:
            self.fitness = ((1 /
                            (1 + exp(phi_age *
                            (self.age - a_half)))) *
                            (1 / (1 + exp(-(phi_weight *
                            (self.weight - w_half))))))
        else:
            self.fitness = 0

    def weight_gain(self, consumption):
        """Gains weight according to a formula using given parameters
        and the input consumption.

        :param consumption: float containing the amount of fodder
        the animal consumes
        :type consumption: float
        """
        beta = self.parameters["beta"]

        self.weight += consumption * beta
        self.fitness_change()

    def can_birth_occur(self):
        """Checks if birth of animal can occur according to two
        probability formulas.

        :return: True if birth can occur, and False if birth can not occur
        :rtype: bool
        """
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
        """Creates an instance of either class Herbivore or Carnivore.
        If the birth does not occur, the class instance gets removed from pop
        """
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
        """Subtracts weight from animal according to formula.
        Changes fitness accordingly.
        """
        eta = self.parameters["eta"]

        self.weight -= eta * self.weight
        self.fitness_change()

    def death(self):
        """Checks if death occurs according to formula and a probability.

        :return: True if death occurs, and False if death does not occur
        :rtype: bool
        """
        omega = self.parameters["omega"]
        death_prob = omega * (1 - self.fitness)

        if self.fitness == 0:
            return True

        elif random.random() <= death_prob: #SJEKK ALLE SANNSYNLIGHETER, om <= blir riktig
            return True

        else:
            return False

    def will_move(self):
        """Checks whether or not the animal is able to move.

        :return: True if animal can move, False if animal can not move
        :rtype: bool
        """
        mu = self.parameters["mu"]

        if random.random() <= mu * self.fitness:
            return True
        else:
            return False

    def get_relevant_fodder(self, loc):
        """Checks if animal is a Herbivore or a Carnivore and with that
        information returns the relevant fodder.

        :param loc: Indicates the coordinate of the animal
        :type loc: tuple
        :return: If Herbivore: number of fodder on loc, if Carnivore:
        total weight of Herbivores on that loc.
        :rtype: float
        """
        if self.__class__.__name__ == "Herbivore":
            return self.island.get_fodder_on_loc(loc)
        elif self.__class__.__name__ == "Carnivore":
            return self.island.get_total_herb_weight_on_loc(loc)

    def get_num_same_species(self, loc):
        """Checks if animal is a Herbivore or Carnivore and with that
        information returns number of animals of same species.

        :param loc: Indicates the coordinate of the animal
        :type loc: tuple
        :return: Number of same species animals on loc
        :rtype: int
        """
        if self.__class__.__name__ == "Herbivore":
            return self.island.get_num_herb_on_loc(loc)
        elif self.__class__.__name__ == "Carnivore":
            return self.island.get_num_carn_on_loc(loc)

    def relative_abundance(self, loc):
        """Returns the relative abundance using given formula.

        :param loc: Indicates the coordinate of the animal
        :type loc: tuple
        :return: Returns relative abundance on given loc
        :rtype: float
        """
        F = self.parameters["F"]
        num_same_species = self.get_num_same_species(loc)
        relevant_fodder = self.get_relevant_fodder(loc)
        relative_abundance = relevant_fodder/((num_same_species + 1) * F)
        return relative_abundance

    def propensity(self, loc):
        """Returns the propensity according to given formula.

        :param loc: Indicates the coordinate of the animal
        :type loc: tuple
        :return: Returns propensity on given loc
        :rtype: int or float
        """
        lambda_ = self.parameters["lambda"]
        relative_abundance = self.relative_abundance(loc)
        cell_type = self.island.get_cell_type(loc)

        if cell_type == "Mountain" or cell_type == "Ocean":
            return 0
        else:
            return exp(lambda_ * relative_abundance)

    def get_potential_coordinates(self):
        """Returns a list of potential nearby coordinates.

        :return: List of 4 tuples that are possible to move to
        :rtype: list
        """
        loc_1 = (self.loc[0] + 1, self.loc[1])
        loc_2 = (self.loc[0] - 1, self.loc[1])
        loc_3 = (self.loc[0], self.loc[1] + 1)
        loc_4 = (self.loc[0], self.loc[1] - 1)
        loc_list = [loc_1, loc_2, loc_3, loc_4]
        return loc_list

    def total_propensity(self, loc_list):
        """Returns the sum of the propensity of the neighbouring coordinates.

        :param loc_list: List of 4 tuples that are possible to move to
        :type loc_list: list
        :return: Sum of propensities
        :rtype: float
        """
        total_propensity = 0
        for loc in loc_list:
            total_propensity += self.propensity(loc)
        return total_propensity

    def probabilities(self, loc_list):
        """Returns a list containing the probability of moving to each of the
        coordinates.

        :param loc_list: List of 4 tuples that are possible to move to
        :type loc_list: list
        :return: Probability list if there is a chance to move, None if not.
        :rtype: list or NoneType
        """
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
        """Makes a random choice of which of the coordinates to move to
        with respect to the probabilities.

        :param loc_list: List of 4 tuples that are possible to move to
        :type loc_list: list
        :return: Coordinate to move to, if animal does not move returns None
        :rtype: tuple or NoneType
        """
        prob_list = self.probabilities(loc_list)
        if prob_list is None:
            return None
        else:
            destination_index = np.random.choice(range(len(loc_list)), p=prob_list)
            destination = loc_list[destination_index]
            return destination

    def migrate(self):
        """If animal moves then it changes the animals coordinates to
        the correct location.
        """
        if self.will_move():
            loc_list = self.get_potential_coordinates()
            destination = self.destination(loc_list)
            if destination is not None:
                self.island.remove_pop_on_loc(self.loc, self)
                self.island.add_pop_on_loc(destination, self)
                self.loc = destination


class Herbivore(Animals):
    """SUMMARY

    :param island: An instance of the :class:'src.biosim.island.Island'
    with data and methods, containing info about the geography.
    :type island: class:'src.biosim.island.Island'
    :param loc: Indicates the coordinates of the animal
    :type loc: tuple
    :param age: Indicates the age of the animal, defaults to 0
    :type age: int, optional
    :param weight: Indicates the weight of the animal, defaults to None
    :type weight: float, optional
    """
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
        """Constructor method.
        """
        super().__init__(island, loc, age, weight)

    def eaten(self):
        """Removes the instance of itself from its location.
        """
        self.island.remove_pop_on_loc(self.loc, self)

    def fodder_eaten(self):
        """Returns the amount of fodder the Herbivore eats

        :raises ValueError: If fodder is negative float.
        :return: Returns amount of fodder eaten
        :rtype: float or int
        """

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
        """Herbivore eats fodder, so the fodder gets subtracted from the
        location, and the Herbivore gains weight accordingly.
        """
        consumed_fodder = self.fodder_eaten()
        self.island.herb_eats_fodder_on_loc(self.loc, consumed_fodder)
        self.weight_gain(consumed_fodder)


class Carnivore(Animals):
    """SUMMARY

    :param island: An instance of the :class:'src.biosim.island.Island'
    with data and methods, containing info about the geography.
    :type island: class:'src.biosim.island.Island'
    :param loc: Indicates the coordinates of the animal
    :type loc: tuple
    :param age: Indicates the age of the animal, defaults to 0
    :type age: int, optional
    :param weight: Indicates the weight of the animal, defaults to None
    :type weight: float, optional
    """

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
        """Constructor method.
        """
        super().__init__(island, loc, age, weight)

    def kill_herb(self, herb):
        """Checks if the Carnivore kills a Herbivore using a parameter
        and the fitness of both the animals.

        :param herb: An instance of the class:'src.biosim.animals.Herbivore'
        containing info about the Herbivore.
        :type herb: class:'src.biosim.animals.Herbivore'
        :return: True if Carnivore kills Herbivore, False if not
        :rtype: bool
        """
        DeltaPhiMax = self.parameters["DeltaPhiMax"]
        herb_fitness = herb.get_fitness()
        fitness_diff = self.fitness - herb_fitness
        if self.fitness <= herb_fitness:
            kill_prob = 0
        elif 0 < fitness_diff < DeltaPhiMax:
            kill_prob = fitness_diff/DeltaPhiMax
        else:
            kill_prob = 1

        if random.random() <= kill_prob:
            return True
        else:
            return False

    def feed(self):
        """Feeds a single Carnivore. Updates the Carnivore weight and
        removes the Herbivore if it is eaten.
        """
        herbs_in_loc = self.island.get_herb_list_on_loc(self.loc)
        herbs_in_loc.sort(key=lambda herb: herb.fitness) # Tries to kill the herbivore with the lowest fitness first
        desired_weight = self.parameters["F"]
        eaten_weight = 0
        index = 0

        while eaten_weight < desired_weight and index < len(herbs_in_loc):
            herb = herbs_in_loc[index]
            if self.kill_herb(herb):
                last_kill = herb.weight
                appetite_weight = self.appetite_checker(
                    eaten_weight, desired_weight, last_kill)
                eaten_weight += appetite_weight
                self.weight_gain(appetite_weight)
                herb.eaten()
            index += 1

    @staticmethod
    def appetite_checker(eaten_weight, desired_weight, last_kill):
        """Checks if the Herbivores weight is higher than the desired weight,
        and returns the amount of food the Carnivore eats.

        :param eaten_weight: The amount of food the Carnivore has eaten before
        before the last Herb-kill
        :type eaten_weight: float
        :param desired_weight: The amount of food the Carnivore wants to eat
        :type desired_weight: float
        :param last_kill: The weight of the dead Herbivore
        :type last_kill: float
        :return: Amount of food Carnivore eats
        :rtype: float
        """
        if eaten_weight + last_kill > desired_weight:
            appetite_weight = desired_weight - eaten_weight
            return appetite_weight
        else:
            return last_kill

