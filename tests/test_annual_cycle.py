# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from island import Island
from animals import Herbivore, Carnivore, Animals
from annual_cycle import AnnualCycle
import pytest
from mock import patch


class TestAnnualCycle:


    @pytest.fixture(autouse=True)
    def setup(self):
        self.i = Island()


    def test_cycle_instance(self):
        i = Island()
        cycle = AnnualCycle(i)

        assert isinstance(cycle, AnnualCycle)

    def test_fodder_growth_refills_fodder(self):
        i = Island()
        loc = (2,7)
        h = Herbivore(i, loc)
        cycle = AnnualCycle(i)
        full_jungle = i.get_fodder_on_loc(loc)
        h.feed()
        refillable_jungle = i.get_fodder_on_loc(loc)
        cycle.fodder_growth()
        refilled_jungle = i.get_fodder_on_loc(loc)

        assert full_jungle > refillable_jungle
        assert full_jungle == refilled_jungle

    def test_sort_by_fitness_sorts(self):
        loc_1 = (2, 7)
        loc_2 = (2, 9)
        i = Island()
        h_1 = Herbivore(i, loc_1, weight=20)
        h_2 = Herbivore(i, loc_2, weight=5)
        h_3 = Herbivore(i, loc_1, weight=100)
        c = AnnualCycle(i)
        manually_sorted_list = [h_3, h_1, h_2]
        c.sort_by_fitness()
        sorted_list = i.get_all_herb_list()

        assert sorted_list == manually_sorted_list

    def test_herb_feeding_changes_weight_for_all_herbs(self):
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2, 9)
        h_1 = Herbivore(i, loc_1)
        h_2 = Herbivore(i, loc_2)
        old_weight_1 = h_1.weight
        old_weight_2 = h_2.weight
        cycle.herb_feeding()
        new_weight_1 = h_1.weight
        new_weight_2 = h_2.weight

        assert old_weight_1 < new_weight_1
        assert old_weight_2 < new_weight_2

    def test_carn_feeding_changes_weight_for_all_carns(self, mocker):
        mocker.patch('random.random', return_value=0)
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2, 9)
        c_1 = Carnivore(i, loc_1, weight=100)
        c_2 = Carnivore(i, loc_2, weight=100)
        h_1 = Herbivore(i, loc_1, weight=10)
        h_2 = Herbivore(i, loc_2, weight=10)
        old_weight_1 = c_1.weight
        old_weight_2 = c_2.weight
        cycle.carn_feeding()
        new_weight_1 = c_1.weight
        new_weight_2 = c_2.weight

        assert old_weight_1 < new_weight_1
        assert old_weight_2 < new_weight_2

    def test_procreation_herb_adds_herb_pop(self, mocker):
        mocker.patch('random.random', return_value=0)
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2,8)
        h_1 = Herbivore(i, loc_1, weight=100)
        h_2 = Herbivore(i, loc_1, weight=100)
        h_3 = Herbivore(i, loc_2, weight=100)
        h_4 = Herbivore(i, loc_2, weight=100)
        old_num_loc_1 = i.get_num_herb_on_loc(loc_1)
        old_num_loc_2 = i.get_num_herb_on_loc(loc_2)
        cycle.procreation_herb()
        new_num_loc_1 = i.get_num_herb_on_loc(loc_1)
        new_num_loc_2 = i.get_num_herb_on_loc(loc_2)

        assert old_num_loc_1 < new_num_loc_1
        assert old_num_loc_2 < new_num_loc_2

    def test_procreation_carn_adds_carn_pop(self, mocker):
        mocker.patch('random.random', return_value=0)
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2,8)
        h_1 = Carnivore(i, loc_1, weight=100)
        h_2 = Carnivore(i, loc_1, weight=100)
        h_3 = Carnivore(i, loc_2, weight=100)
        h_4 = Carnivore(i, loc_2, weight=100)
        old_num_loc_1 = i.get_num_carn_on_loc(loc_1)
        old_num_loc_2 = i.get_num_carn_on_loc(loc_2)
        cycle.procreation_carn()
        new_num_loc_1 = i.get_num_carn_on_loc(loc_1)
        new_num_loc_2 = i.get_num_carn_on_loc(loc_2)

        assert old_num_loc_1 < new_num_loc_1
        assert old_num_loc_2 < new_num_loc_2

    def test_procreation_all_adds_all_pop(self, mocker):
        mocker.patch('random.random', return_value=0)
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2,8)
        h_1 = Carnivore(i, loc_1, weight=100)
        h_2 = Carnivore(i, loc_1, weight=100)
        h_3 = Herbivore(i, loc_2, weight=100)
        h_4 = Herbivore(i, loc_2, weight=100)
        old_num_loc_1 = i.get_num_carn_on_loc(loc_1)
        old_num_loc_2 = i.get_num_herb_on_loc(loc_2)
        cycle.procreation_all()
        new_num_loc_1 = i.get_num_carn_on_loc(loc_1)
        new_num_loc_2 = i.get_num_herb_on_loc(loc_2)

        assert old_num_loc_1 < new_num_loc_1
        assert old_num_loc_2 < new_num_loc_2

    def test_aging_adds_1_year_to_all_animals(self):
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2,8)
        h_1 = Carnivore(i, loc_1, weight=100, age=0)
        h_2 = Carnivore(i, loc_1, weight=100, age=0)
        h_3 = Herbivore(i, loc_2, weight=100, age=0)
        h_4 = Herbivore(i, loc_2, weight=100, age=0)
        a_list = [h_1, h_2, h_3, h_4]
        cycle.aging()

        for animal in a_list:
            assert animal.age == 1

    def test_weight_loss_changes_for_all_animals(self, mocker):
        mocker.patch('random.random', return_value=0)
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2,8)
        c_1 = Carnivore(i, loc_1, weight=100)
        h_1 = Herbivore(i, loc_2, weight=100)
        old_weight_1 = c_1.weight
        old_weight_2 = h_1.weight
        cycle.weight_loss()

        assert c_1.weight < old_weight_1
        assert h_1.weight < old_weight_2


    def test_animal_death_removes_all_dead_animals(self, mocker):
        mocker.patch('random.random', return_value=0)
        i = Island()
        cycle = AnnualCycle(i)
        loc_1 = (2, 7)
        loc_2 = (2, 8)
        c_1 = Carnivore(i, loc_1, weight=100)
        h_1 = Herbivore(i, loc_2, weight=100)
        old_herb_count = i.get_num_herb_on_loc(loc_2)
        old_carn_count = i.get_num_carn_on_loc(loc_1)
        cycle.animal_death()

        assert i.get_num_herb_on_loc(loc_2) < old_herb_count
        assert i.get_num_carn_on_loc(loc_1) < old_carn_count

    @patch.object(Herbivore, 'will_move')
    @patch.object(Carnivore, 'will_move')
    def test_migration_moves_all_animals(self, mocker_1, mocker_2):
        mocker_1.return_value = True
        mocker_2.return_value = True
        geogr = """\
                               OOOO
                               OJJO
                               OOOO"""
        i = Island(geogr)
        cycle = AnnualCycle(i)
        old_loc = (1, 1)
        new_loc = (1, 2)
        h = Herbivore(i, old_loc)
        c = Carnivore(i, old_loc)
        cycle.migration()

        assert h.get_loc() == new_loc
        assert c.get_loc() == new_loc
