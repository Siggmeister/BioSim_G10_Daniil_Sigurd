# -*- coding: utf-8 -*-
import textwrap
from landscape import *
import numpy as np


class Island:

    default_geogr = """\
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

    def __init__(self, geo_string=None):
        if geo_string is None:
            geo_string = Island.default_geogr
        self._check_geo_string(geo_string)
        self.island_dict = self._island_dict_maker(geo_string)

    def fodder_annual_refill(self):
        for loc in self.island_dict:
            self.island_dict[loc].fodder_annual_refill()

    def get_fodder_on_loc(self, loc):
        return self.island_dict[loc].get_fodder()

    def get_herb_list_on_loc(self, loc):
        return self.island_dict[loc].get_herb_pop_list()

    def get_carn_list_on_loc(self, loc):
        return self.island_dict[loc].get_carn_pop_list()

    def add_pop_on_loc(self, loc, animal):
        self.island_dict[loc].add_pop(animal)

    def remove_pop_on_loc(self, loc, animal):
        self.island_dict[loc].remove_pop(animal)

    def get_num_herb_on_loc(self, loc):
        return self.island_dict[loc].get_num_herb()

    def get_num_carn_on_loc(self, loc):
        return self.island_dict[loc].get_num_carn()

    def herb_eats_fodder_on_loc(self, loc, fodder_eaten):
        self.island_dict[loc].herb_eats_fodder(fodder_eaten)

    def sort_all_animals_by_fitness(self):
        for loc in self.island_dict:
            self.island_dict[loc].sort_pop_by_fitness()

    def get_all_herb_list(self):
        all_herb_list = []
        for loc in self.island_dict:
            all_herb_list.extend(self.get_herb_list_on_loc(loc))
        return all_herb_list

    def get_all_carn_list(self):
        all_carn_list = []
        for loc in self.island_dict:
            all_carn_list.extend(self.get_carn_list_on_loc(loc))
        return all_carn_list

    def get_total_herb_weight_on_loc(self, loc):
        return self.island_dict[loc].get_total_herb_weight()

    def get_cell_type(self, loc):
        return self.island_dict[loc].__class__.__name__

    @staticmethod
    def _check_geo_string(geo_string):
        geo_string = textwrap.dedent(geo_string)
        geo_list = [list(line) for line in geo_string.splitlines()]
        for line in geo_list:
            if len(line) != len(geo_list[0]):
                raise ValueError("The map string has to be of rectangular shape!")

        geo_matrix = np.array(geo_list)
        top_slice = geo_matrix[0, :]
        bottom_slice = geo_matrix[-1, :]
        left_slice = geo_matrix[:, 0]
        right_slice = geo_matrix[:, -1]
        whole_frame_array = np.concatenate((top_slice, bottom_slice, left_slice, right_slice), axis=None)

        for geo in whole_frame_array:
            if geo != "O":
                raise ValueError("The edges of the map must be all ocean type!")


    @staticmethod
    def _island_dict_maker(geo_string):
        geo_string = textwrap.dedent(geo_string)
        geo_list = [list(line) for line in geo_string.splitlines()]
        island_dict = {}

        for i, line in enumerate(geo_list):
            for j, landscape_code in enumerate(line):
                if landscape_code == "O":
                    geo = Ocean()
                elif landscape_code == "J":
                    geo = Jungle()
                elif landscape_code == "M":
                    geo = Mountain()
                elif landscape_code == "S":
                    geo = Savannah()
                elif landscape_code == "D":
                    geo = Desert()
                island_dict[(i, j)] = geo

        return island_dict

    @staticmethod
    def _param_changer(landscape, new_param):
        Landscape.param_changer(landscape, new_param)
