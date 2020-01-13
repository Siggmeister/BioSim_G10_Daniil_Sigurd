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
        self.island = Island(self.geogr)
        jungle_loc = (2,7)
        self.stnd_herb = Herbivore(self.island, jungle_loc)


    def test_fitness_change_for_set_weight(self):
        jungle_loc = (2,7)
        s_1 = Herbivore(self.island, jungle_loc, weight=3)
        s_2 = Herbivore(self.island, jungle_loc, weight=5)
        s_3 = Herbivore(self.island, jungle_loc, weight=7)
        s_1.fitness_change()
        s_2.fitness_change()
        s_3.fitness_change()

        assert s_1.fitness == pytest.approx(0.331, 0.01)
        assert s_2.fitness == pytest.approx(0.377, 0.01)
        assert s_3.fitness == pytest.approx(0.425, 0.01)
        #Sjekk med sannsynlighet

    def test_fodder_eaten_for_full_landscapes(self):
        jungle_loc = (2,7)
        savannah_loc = (2,1)
        ocean_loc = (0,0)
        j_sim = Herbivore(self.island, jungle_loc)
        j_sim.fodder_eaten()
        s_sim = Herbivore(self.island, savannah_loc)
        s_sim.fodder_eaten()
        o_sim = Herbivore(self.island, ocean_loc)
        o_sim.fodder_eaten()

        assert j_sim.fodder_eaten() == 10
        assert s_sim.fodder_eaten() == 10
        assert o_sim.fodder_eaten() == 0

    def test_fodder_eaten_only_eat_available_fodder(self):
        jungle_loc = (2,7)
        Island.param_changer("J", {"f_max" : 5})
        i_sim = Island(self.geogr)
        s_1 = Herbivore(i_sim, jungle_loc)

        assert s_1.fodder_eaten() == 5

    def test_fodder_eaten_raises_error(self):
        jungle_loc = (2, 7)
        Island.param_changer("J", {"f_max" : -100})
        i_sim = Island(self.geogr)
        s_1 = Herbivore(i_sim, jungle_loc)
        #s_1.fodder_eaten() SJEKK UT

        self.assertRaises(ValueError, s_1.fodder_eaten)

    def test_weight_gain_properly(self):
        jungle_loc = (2,7)
        chosen_weight = 5
        i = Herbivore(self.island, jungle_loc, weight = chosen_weight)
        fodder_eaten = Animals.animal_parameters["Herbivore"]["F"]
        beta = Animals.animal_parameters["Herbivore"]["beta"]
        i.weight_gain(fodder_eaten)

        assert i.weight == chosen_weight+fodder_eaten*beta

    def test_feed_changes_fitness(self):

        start_fitness = self.stnd_herb.fitness
        self.stnd_herb.feed()
        changed_fitness = self.stnd_herb.fitness

        assert start_fitness != changed_fitness

    def test_count_all_herb_in_current_loc_gives_correct_amount(self):
        loc_1 = (2,7)
        loc_2 = (1, 1)
        herb_loc_1 = Herbivore(self.island, loc_1)
        herb_loc_2 = Herbivore(self.island, loc_2)
        herb_list = [herb_loc_1 for _ in range(3)]


        assert herb_loc_1.count_all_herb_in_current_loc(herb_list) == 3
        assert herb_loc_2.count_all_herb_in_current_loc(herb_list) == 0

    def test_can_birth_occur_with_1_herbivore(self):
        herb_list_len_1 = [self.stnd_herb]

        assert self.stnd_herb.can_birth_occur(herb_list_len_1) == False

    def test_can_birth_occur_with_5_herbivores(self, mocker):
        mocker.patch('random.random', return_value=0.1)
        herb_list = [self.stnd_herb for _ in range(5)]

        assert self.stnd_herb.can_birth_occur(herb_list) == True
