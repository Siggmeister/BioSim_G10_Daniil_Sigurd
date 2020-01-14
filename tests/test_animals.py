# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from src.biosim.animals import *
from src.biosim.island import *
from src.biosim.landscape import *
from src.biosim.annual_cycle import *
import pytest



class TestAnimals:

    def test_aging(self):
        i = Island()
        s = Animals(island=i, loc=(0, 0))
        s.aging()

        assert s.age == 1
        s.age = 0

        for _ in range(5):
            s.aging()

        assert s.age == 5

    def test_get_loc_returns_loc(self):
        i = Island()
        loc = (1,1)
        s = Animals(i, loc)

        assert s.get_loc() == loc

    def test_get_fitness_returns_fitness(self):
        i = Island()
        loc = (1,1)
        s_1 = Herbivore(i, loc, weight = 0)
        s_2 = Herbivore(i, loc, weight = 5)


        assert s_1.get_fitness() == 0
        assert s_2.get_fitness() == pytest.approx(0.377, 0.01)

    def test_param_changer_changes_correctly(self):
        i = Island()
        loc = (1, 1)
        s = Animals(i, loc)
        old_param = s.animal_parameters["Herbivore"]["F"]
        s.param_changer("Herbivore", {"F" : 20})
        new_param = s.animal_parameters["Herbivore"]["F"]

        assert old_param != new_param
        s.param_changer("Herbivore", {"F": 10})

class TestHerbivore:

    @pytest.fixture(autouse=True)
    def setup(self):
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
        optimal_fodder = self.animal_parameters["Herbivore"]["F"]

        assert j_sim.fodder_eaten() == optimal_fodder
        assert s_sim.fodder_eaten() == optimal_fodder
        assert o_sim.fodder_eaten() == 0


    def test_fodder_eaten_only_eat_available_fodder(self):
        jungle_loc = (2,7)
        Island._param_changer("J", {"f_max" : 5})
        i_sim = Island(self.geogr)
        s_1 = Herbivore(i_sim, jungle_loc)

        assert s_1.fodder_eaten() == 5

    def test_fodder_eaten_raises_error(self):
        jungle_loc = (2, 7)
        Island._param_changer("J", {"f_max" : -100})
        i_sim = Island(self.geogr)
        s_1 = Herbivore(i_sim, jungle_loc)
        #s_1.fodder_eaten() #SJEKK UT

        with pytest.raises(ValueError):
            s_1.fodder_eaten()
        #Island.param_changer("J", {"f_max": 800})

    def test_weight_gain_properly(self):
        jungle_loc = (2,7)
        chosen_weight = 5
        i = Herbivore(self.island, jungle_loc, weight = chosen_weight)
        fodder_eaten = Animals.animal_parameters["Herbivore"]["F"]
        beta = Animals.animal_parameters["Herbivore"]["beta"]
        i.weight_gain(fodder_eaten)

        assert i.weight == chosen_weight+fodder_eaten*beta

    def test_feed_changes_fitness(self):
        loc = (2,1)
        i_sim = Herbivore(self.island, loc)
        start_fitness = i_sim.fitness
        i_sim.feed()
        changed_fitness = i_sim.fitness

        assert start_fitness != changed_fitness

    def test_can_birth_occur_with_1_herbivore(self):
        loc = (2,7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc)
        i_sim.add_pop_on_loc(loc, a_sim)

        assert not self.stnd_herb.can_birth_occur()

    def test_can_birth_occur_with_5_herbivores_with_1_prob(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight = 100)
        for _ in range(5):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert a_sim.can_birth_occur()

    def test_can_birth_occur_with_5_herbivores_with_0_prob(self, mocker):
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight=100)
        for _ in range(5):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert not a_sim.can_birth_occur()

    def test_birth_adds_to_pop_list(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight=100)
        herb_pop_list = [a_sim, a_sim]
        #for _ in range(3):
        a_sim.birth(herb_pop_list)
        a = AnnualCycle(herb_pop_list, [], i_sim)

        #assert i_sim.get_herb_pop_on_loc(loc) == 5
        #assert len(herb_pop_list) == 3
        assert len(a.herb_pop_list) == 3
