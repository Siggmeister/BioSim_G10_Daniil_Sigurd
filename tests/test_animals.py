# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from src.biosim.animals import *
from src.biosim.island import *
from unittest import TestCase
import pytest


class TestAnimals:

    def test_aging(self):
        s = Animals(loc=(0,0))
        s.aging()

        assert s.age == 1
        s.age = 0

        for _ in range(5):
            s.aging()

        assert s.age == 5

class TestHerbivore(TestCase):

    def setUp(self):
        self.landscape_parameters = {"J": {"f_max": 800.0},
                                     "S": {"f_max": 300.0,
                                           "alpha": 0.3}}

        self.animal_parameters = {"Herbivore": {"w_birth": 8.0,
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

        self.geogr = """\
                           OOOOOOOOOOOOOOOOOOOOO
                           OOOOOOOOSMMMMJJJJJJJO
                           OSSSSSJJJJMMJJJJJJJOO
                           OSSSSSSSSSMMJJJJJJOOO
                           OSSSSSJJJJJJJJJJJJOOO
                           OSSSSSJJJDDJJJSJJJOOO
                           OSSJJJJJDDDJJJSSSSOOO
                           OOSSSSJJJDDJJJSOOOOOO
                           OSSSJJJJJDDJJJJJJJOOO
                           OSSSSJJJJDDJJJJOOOOOO
                           OOSSSSJJJJJJJJOOOOOOO
                           OOOSSSSJJJJJJJOOOOOOO
                           OOOOOOOOOOOOOOOOOOOOO"""

        self.herb_params = self.animal_parameters["Herbivore"]
        self.island = Island(self.geogr, self.landscape_parameters)


    def test_fitness_change_for_set_weight(self):
        jungle_loc = (2,7)
        s_1 = Herbivore(self.island, self.herb_params, jungle_loc, weight=3)
        s_2 = Herbivore(self.island, self.herb_params, jungle_loc, weight=5)
        s_3 = Herbivore(self.island, self.herb_params, jungle_loc, weight=7)
        s_1.fitness_change()
        s_2.fitness_change()
        s_3.fitness_change()

        assert s_1.fitness == pytest.approx(0.331, 0.01)
        assert s_2.fitness == pytest.approx(0.377, 0.01)
        assert s_3.fitness == pytest.approx(0.425, 0.01)
        #Sjekk med sannsynlighet



    def test_fodder_eaten_raises_error(self):
        jungle_loc = (2, 7)
        i_sim = Island(self.geogr, self.landscape_parameters)
        i_sim.island_dict[jungle_loc]["Fodder"] = -100#sjekk
        #i_sim.get_fodder_on_loc() = -100  # sjekk
        s_1 = Herbivore(self.island, self.herb_params, jungle_loc)
        s_1.fodder_eaten()

        self.assertRaises(ValueError, s_1.fodder_eaten())
        #assert s_1.fodder_eaten() == i_sim.get_fodder_on_loc(jungle_loc)










