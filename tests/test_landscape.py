
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
        land = Landscape()
        land.add_pop(herb)
        assert herb in land.herb_pop_list
        land.remove_pop(herb)
        assert herb not in land.herb_pop_list

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






