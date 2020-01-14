# -*- coding: utf-8 -*-
import textwrap
from landscape import *
import numpy as np


class Island:

    landscape_parameters = {"J": {"f_max": 800.0},
                                 "S": {"f_max": 300.0,
                                       "alpha": 0.3}}

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


i = Island()



