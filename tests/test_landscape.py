
from src.biosim.animals import *
from src.biosim.island import *
from src.biosim.landscape import *
from src.biosim.annual_cycle import *
import pytest


class Test_Landscape:

    def test_landscape_instance(self):
        land = Landscape()
        assert isinstance(land, Landscape)

    def test_add_pop(self):
        herb = Herbivore(Island(), (0,0))
        land = Landscape()
        assert len(land.herb_pop_list) == 0
        land.add_pop(herb)
        assert herb in land.herb_pop_list

    def test_remove_pop(self):
        herb = Herbivore(Island(), (0,0))
        carn = Carnivore(Island(), (0,0))
        land = Landscape()
        land.add_pop(herb)
        land.add_pop(carn)
        assert herb in land.herb_pop_list
        assert carn in land.carn_pop_list
        land.remove_pop(herb)
        land.remove_pop(carn)
        assert herb not in land.herb_pop_list
        assert carn not in land.carn_pop_list

    def test_fodder_annual_refill(self):
        land = Landscape()
        land.fodder_annual_refill()

    def test_get_fodder(self):
        land = Landscape()
        land.fodder = 200
        assert land.get_fodder() == land.fodder

    def test_get_availability(self):
        land = Landscape()
        assert land.get_availability() == land.available

    def test_get_pop_lists(self):
        land = Landscape()
        land.herb_pop_list.append(Herbivore(Island(), (0,0)))
        land.carn_pop_list.append(Carnivore(Island(), (0,0)))
        assert land.get_herb_pop_list() == land.herb_pop_list
        assert land.get_carn_pop_list() == land.carn_pop_list

    def test_get_num_animals(self):
        land = Landscape()
        num_herb = 3
        num_carn = 2

        for _ in range(num_herb):
            land.add_pop(Herbivore(Island(), (0,0)))

        for _ in range(num_carn):
            land.add_pop(Carnivore(Island(), (0,0)))

        assert land.get_num_herb() == num_herb
        assert land.get_num_carn() == num_carn

    def test_param_changer(self):
        land = Landscape()
        landscape = "J"
        new_param = {"f_max": 700}
        land.param_changer(landscape, new_param)
        assert land.landscape_parameters[landscape]["f_max"] == new_param["f_max"]

    def test_sort_pop_by_fitness(self):
        land = Landscape()
        herb_list = []
        carn_list = []
        for _ in range(3):
            herb = Herbivore(Island(), (0,0))
            carn = Carnivore(Island(), (0,0))
            herb_list.append(herb)
            carn_list.append(carn)
            land.add_pop(herb)
            land.add_pop(carn)

        herb_list.sort(key=lambda herb: herb.fitness, reverse=True)
        carn_list.sort(key=lambda carn: carn.fitness, reverse=True)
        land.sort_pop_by_fitness()

        assert land.get_herb_pop_list() == herb_list
        assert land.get_carn_pop_list() == carn_list

    def test_get_total_herb_weight(self):
        land = Landscape()
        assert land.get_total_herb_weight() == 0
        herb_1 = Herbivore(Island(), (0,0))
        land.add_pop(herb_1)
        assert land.get_total_herb_weight() == herb_1.weight
        herb_2 = Herbivore(Island(), (0,0))
        land.add_pop(herb_2)
        assert land.get_total_herb_weight() == herb_1.weight + herb_2.weight

class TestJungle:

    def test_jungle_instance(self):
        j = Jungle()
        assert isinstance(j, Landscape)
        assert isinstance(j, Jungle)

    def test_initial_fodder(self):
        j = Jungle()
        assert j.get_fodder() == j.landscape_parameters["J"]["f_max"]

    def test_fodder_annual_refill_jungle(self):
        j = Jungle()
        j.fodder = 400
        j.fodder_annual_refill()
        assert j.get_fodder() == j.landscape_parameters["J"]["f_max"]

    def test_herb_eats_fodder(self):
        j = Jungle()
        f_max = j.landscape_parameters["J"]["f_max"]
        herb_amount = 10
        j.herb_eats_fodder(herb_amount)
        assert j.get_fodder() == f_max - herb_amount




class TestSavannah:

    def test_savannah_instance(self):
        s = Savannah()
        assert isinstance(s, Landscape)
        assert isinstance(s, Savannah)

    def test_inital_fodder(self):
        s = Savannah()
        assert s.get_fodder() == s.landscape_parameters["S"]["f_max"]

    def test_fodder_annual_refill_savannah(self):
        s = Savannah()
        s.fodder = 0
        expected_after_refill = 90
        s.fodder_annual_refill()
        assert s.get_fodder() == expected_after_refill

    def test_savannah_can_not_be_over_max(self):
        s = Savannah()
        f_max = s.landscape_parameters["S"]["f_max"]
        s.fodder = f_max + 100
        s.fodder_annual_refill()
        assert s.get_fodder() == f_max

class TestDesert:

    def test_desert_instance(self):
        d = Desert()
        assert isinstance(d, Landscape)
        assert isinstance(d, Desert)


class TestOcean:

    def test_ocean_instance(self):
        o = Ocean()
        assert isinstance(o, Landscape)
        assert isinstance(o, Ocean)


class TestMountain:

    def test_ocean_instance(self):
        m = Mountain()
        assert isinstance(m, Landscape)
        assert isinstance(m, Mountain)