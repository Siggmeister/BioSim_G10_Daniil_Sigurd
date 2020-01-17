# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import *
import pytest
from mock import patch


class TestAnimals:

    @pytest.fixture(autouse=True)
    def setup(self):

        self.i = Island()
        self.loc = (0,0)
        stnd_herb = Herbivore(island=self.i, loc=self.loc)
        stnd_carn = Carnivore(island=self.i, loc=self.loc)
        self.stnd_a_list = [stnd_herb, stnd_carn]

        self.herb_w_0 = Herbivore(island=self.i, loc=self.loc, weight = 0)
        self.herb_w_5 = Herbivore(island=self.i, loc=self.loc, weight = 5)

        self.carn_w_0 = Carnivore(island=self.i, loc=self.loc, weight=0)
        self.carn_w_5 = Carnivore(island=self.i, loc=self.loc, weight=5)
        self.carn_w_7 = Carnivore(island=self.i, loc=self.loc, weight=7)

        self.a_list_w_0 = [self.herb_w_0, self.carn_w_0]
        self.a_list_w_5 = [self.herb_w_5, self.carn_w_5]

    def test_get_right_params_herb(self):
        assert Herbivore.parameters["beta"] == 0.9
        assert Herbivore.parameters["a_half"] == 40.0
        assert Herbivore.parameters["lambda"] == 1.0
        assert Herbivore.parameters["F"] == 10.0

    def test_get_right_params_carn(self):
        assert Carnivore.parameters["beta"] == 0.75
        assert Carnivore.parameters["a_half"] == 60.0
        assert Carnivore.parameters["lambda"] == 1.0
        assert Carnivore.parameters["F"] == 50.0

    def test_aging(self):
        for a in self.stnd_a_list:
            a.aging()

            assert a.age == 1
            a.age = 0

            for _ in range(5):
                a.aging()

            assert a.age == 5

    def test_get_loc_returns_loc(self):
        for a in self.stnd_a_list:

            assert a.get_loc() == self.loc

    def test_get_fitness_returns_fitness(self):
        for a in self.a_list_w_0:
            assert a.get_fitness() == 0

        assert self.herb_w_5.get_fitness() == pytest.approx(0.377, 0.01)
        assert self.carn_w_5.get_fitness() == pytest.approx(0.598, 0.01)

    def test_param_changer_changes_correctly(self):
        i = Island()
        loc = (1, 1)
        s = Herbivore(i, loc)
        old_param = s.parameters["F"]
        s.param_changer({"F" : 20})
        new_param = s.parameters["F"]

        assert old_param != new_param
        s.param_changer({"F": 10})

    def test_fitness_change_for_set_weight(self):
        self.herb_w_5.fitness_change()
        self.carn_w_5.fitness_change()
        self.carn_w_7.fitness_change()
        self.herb_w_0.fitness_change()
        self.carn_w_0.fitness_change()

        assert self.herb_w_5.fitness == pytest.approx(0.377, 0.01)
        assert self.carn_w_5.fitness == pytest.approx(0.598, 0.01)
        assert self.carn_w_7.fitness == pytest.approx(0.768, 0.01)
        assert self.herb_w_0.fitness == 0
        assert self.carn_w_0.fitness == 0

    def test_weight_gain_properly(self):
        fodder_eaten = Herbivore.parameters["F"]
        beta = Herbivore.parameters["beta"]
        self.herb_w_5.weight_gain(fodder_eaten)

        assert self.herb_w_5.weight == 5+(fodder_eaten*beta)

    def test_feed_changes_fitness(self):
        loc = (2,1)
        i = Island()
        i_sim = Herbivore(i, loc)
        start_fitness = i_sim.fitness
        i_sim.feed()
        changed_fitness = i_sim.fitness

        assert start_fitness != changed_fitness


    def test_can_birth_occur_with_1_herbivore(self):
        loc = (2,7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc)
        i_sim.add_pop_on_loc(loc, a_sim)

        assert not a_sim.can_birth_occur()

    def test_can_birth_occur_with_2_herbivores_with_1_prob(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight = 100)
        for _ in range(2):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert a_sim.can_birth_occur()

    def test_can_birth_occur_with_2_carnivores_with_1_prob(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Carnivore(i_sim, loc, weight=100)
        for _ in range(2):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert a_sim.can_birth_occur()

    def test_can_birth_occur_with_2_herbivores_with_0_prob(self, mocker):
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight=100)
        for _ in range(2):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert not a_sim.can_birth_occur()

    def test_birth_adds_to_num_herb_on_loc(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim_1 = Herbivore(i_sim, loc, weight=100)
        a_sim_2 = Herbivore(i_sim, loc, weight=100)

        a_sim_1.birth()

        assert i_sim.get_num_herb_on_loc(loc) == 3

    def test_birth_adds_to_num_carn_on_loc(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim_1 = Carnivore(i_sim, loc, weight=100)
        a_sim_2 = Carnivore(i_sim, loc, weight=100)

        a_sim_1.birth()

        assert i_sim.get_num_carn_on_loc(loc) == 3

    def test_birth_does_not_happen_if_prob_0(self, mocker):
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        a_sim_1 = Herbivore(i_sim, loc, weight=100)
        a_sim_2 = Herbivore(i_sim, loc, weight=100)

        a_sim_1.birth()

        assert i_sim.get_num_herb_on_loc(loc) == 2

    @patch.object(Herbivore, 'can_birth_occur')
    def test_birth_does_not_add_new_baby_if_weight_too_low(self, mocker):
        a_sim_1 = Herbivore(self.i, self.loc, weight=1)
        mocker.return_value = True
        a_sim_2 = Herbivore(self.i, self.loc, weight=1)
        old_pop = a_sim_1.get_num_same_species(self.loc)
        a_sim_1.birth()
        new_pop = a_sim_1.get_num_same_species(self.loc)

        assert old_pop == new_pop

    def test_annual_weight_loss_decreases_properly(self):
        loc = (2,7)
        i = Island()
        a_sim = Herbivore(i, loc)
        initial_weight = a_sim.weight
        a_sim.annual_weight_loss()
        new_weight = a_sim.weight

        assert initial_weight > new_weight

    def test_death_occurs_if_fitness_is_0(self):
        loc = (2, 7)
        i = Island()
        h_sim = Herbivore(i, loc, weight=0)
        c_sim = Carnivore(i, loc, weight=0)


        assert h_sim.death()
        assert c_sim.death()

    def test_death_occurs_if_prob_is_1(self, mocker):
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        h_sim = Herbivore(i_sim, loc)
        c_sim = Carnivore(i_sim, loc)

        assert h_sim.death()
        assert c_sim.death()

    def test_death_does_not_occur_if_prob_is_(self, mocker):
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        h_sim = Herbivore(i_sim, loc)
        c_sim = Carnivore(i_sim, loc)

        assert not h_sim.death()
        assert not c_sim.death()

    def test_will_move_does_not_happen_if_prob_0(self, mocker):
        mocker.patch('random.random', return_value=1)
        a_sim = Herbivore(self.i, self.loc)

        assert not a_sim.will_move()

    def test_will_move_happens_if_prob_1(self, mocker):
        mocker.patch('random.random', return_value=0)
        a_sim = Herbivore(self.i, self.loc)

        assert a_sim.will_move()

    def test_get_relevant_fodder_herb(self):
        jungle_loc = (2,7)
        a = Herbivore(self.i, jungle_loc)
        fodder = self.i.get_fodder_on_loc(jungle_loc)

        assert a.get_relevant_fodder(jungle_loc) == fodder

    def test_get_relevant_fodder_carn(self):
        i = Island()
        c = Carnivore(i, self.loc)
        herb_weight = 50
        h = Herbivore(i, self.loc, weight=herb_weight)

        assert c.get_relevant_fodder(self.loc) == herb_weight

    def test_get_num_same_species_herb(self):
        i = Island()
        h_1 = Herbivore(i, self.loc)
        h_2 = Herbivore(i, self.loc)

        assert h_1.get_num_same_species(self.loc) == 2

    def test_get_num_same_species_carn(self):
        i = Island()
        h_1 = Carnivore(i, self.loc)
        h_2 = Carnivore(i, self.loc)

        assert h_1.get_num_same_species(self.loc) == 2

    def test_relative_abundance_gives_correct_output_herb(self):
        i = Island()
        jungle_loc = (2,7)
        h = Herbivore(i, jungle_loc)
        self_calculated_abundance = 40
        assert h.relative_abundance(jungle_loc) == self_calculated_abundance

    def test_relative_abundance_gives_correct_output_carn(self):
        i = Island()
        jungle_loc = (2,7)
        h = Herbivore(i, jungle_loc, weight = 50)
        c = Carnivore(i, jungle_loc)
        self_calculated_abundance = 0.5
        assert c.relative_abundance(jungle_loc) == self_calculated_abundance





class TestHerbivore:

    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_fodder_eaten_for_full_landscapes(self):
        jungle_loc = (2,7)
        savannah_loc = (2,1)
        ocean_loc = (0,0)
        i = Island()
        j_sim = Herbivore(i, jungle_loc)
        j_sim.fodder_eaten()
        s_sim = Herbivore(i, savannah_loc)
        s_sim.fodder_eaten()
        o_sim = Herbivore(i, ocean_loc)
        o_sim.fodder_eaten()
        optimal_fodder = Herbivore.parameters["F"]

        assert j_sim.fodder_eaten() == optimal_fodder
        assert s_sim.fodder_eaten() == optimal_fodder
        assert o_sim.fodder_eaten() == 0

    def test_fodder_eaten_only_eat_available_fodder(self):
        jungle_loc = (2,7)
        Island._param_changer("J", {"f_max" : 5})
        i_sim = Island()
        s_1 = Herbivore(i_sim, jungle_loc)

        assert s_1.fodder_eaten() == 5

    def test_fodder_eaten_raises_error(self):
        jungle_loc = (2, 7)
        Island._param_changer("J", {"f_max" : -100})
        i_sim = Island()
        s_1 = Herbivore(i_sim, jungle_loc)

        with pytest.raises(ValueError):
            s_1.fodder_eaten()

    def test_eaten_removes_herb_properly(self):
        i = Island()
        loc = (2, 7)
        a = Herbivore(i, loc)


class TestCarnivore:
    pass