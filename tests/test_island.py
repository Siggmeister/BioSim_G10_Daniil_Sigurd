# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from src.biosim.island import *
from unittest import TestCase
import pytest

class TestIsland(TestCase):
    landscape_parameters = {"J": {"f_max": 800.0},
                            "S": {"f_max": 300.0,
                                  "alpha": 0.3}}

    def setUp(self):
        geo_string = """\
                OOOOO
                OJSMO
                OOOOO
                """
        self.island = Island(geo_string)

    def test_island_instance(self):

        assert isinstance(self.island, Island)

    def test_inital_fodder(self):

        for loc in self.island.island_dict:
            current_fodder = self.island.island_dict[loc]["Fodder"]
            loc_type = self.island.island_dict[loc]["Type"]
            if loc_type == "O" or loc_type == "M":
                assert current_fodder == 0
            else:
                max_fodder = TestIsland.landscape_parameters[loc_type]["f_max"]
                assert current_fodder == max_fodder

    def test_annual_fodder_refill(self):

        for loc in self.island.island_dict:
            loc_type = self.island.island_dict[loc]["Type"]
            if loc_type == "S":
                self.island.island_dict[loc]["Fodder"] = 0
                self.island.fodder_annual_refill()
                assert self.island.island_dict[loc]["Fodder"] > 0
                assert self.island.island_dict[loc]["Fodder"] <= TestIsland.landscape_parameters["S"]["f_max"]
            elif loc_type == "J":
                self.island.island_dict[loc]["Fodder"] = 0
                self.island.fodder_annual_refill()
                assert self.island.island_dict[loc]["Fodder"] == TestIsland.landscape_parameters["J"]["f_max"]

    def test_get_fodder_on_loc(self):
        for loc in self.island.island_dict:
            assert self.island.get_fodder_on_loc(loc) == self.island.island_dict[loc]["Fodder"]

    def test_herb_eats_fodder(self):
        fodder_eaten = 10
        loc = (1,1)
        jungle_cell_fodder_unchanged = self.island.island_dict[loc]["Fodder"]
        self.island.herb_eats_fodder(loc, fodder_eaten)
        assert self.island.island_dict[loc]["Fodder"] == (jungle_cell_fodder_unchanged-fodder_eaten)

    def test_savannah_fodder_over_max(self):
        savannah_loc = (1,2)
        savannah_max_fodder = TestIsland.landscape_parameters["S"]["f_max"]
        self.island.island_dict[savannah_loc]["Fodder"] = savannah_max_fodder + 10
        self.island.fodder_annual_refill()

        assert self.island.island_dict[savannah_loc]["Type"] == "S"
