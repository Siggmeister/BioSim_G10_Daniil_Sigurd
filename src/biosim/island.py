# -*- coding: utf-8 -*-
import textwrap


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

    def __init__(self, geo_string):
        if geo_string is None:
            geo_string = Island.default_geogr
        self.island_dict = self._island_dict_maker(geo_string)
        self.initial_fodder()

    def initial_fodder(self):
        f_max_jungle = Island.landscape_parameters["J"]["f_max"]
        f_max_savannah = Island.landscape_parameters["S"]["f_max"]

        for loc in self.island_dict:
            geo_type = self.island_dict[loc]["Type"]
            if geo_type == "J":
                self.island_dict[loc]["Fodder"] = f_max_jungle #Sjekk
            elif geo_type == "S":
                self.island_dict[loc]["Fodder"] = f_max_savannah

    def fodder_annual_refill(self):
        f_max_jungle = Island.landscape_parameters["J"]["f_max"]
        f_max_savannah = Island.landscape_parameters["S"]["f_max"]
        alpha = Island.landscape_parameters["S"]["alpha"]

        for loc in self.island_dict:
            current_fodder = self.island_dict[loc]["Fodder"]
            geo_type = self.island_dict[loc]["Type"]
            if geo_type == "J":
                current_fodder = f_max_jungle
            elif geo_type == "S":
                current_fodder += (alpha * (f_max_savannah-current_fodder))
                if current_fodder > f_max_savannah:
                    current_fodder = f_max_savannah
            self.island_dict[loc]["Fodder"] = current_fodder

    def get_fodder_on_loc(self, loc):
        return self.island_dict[loc]["Fodder"]

    def herb_eats_fodder(self, loc, fodder_eaten):
        self.island_dict[loc]["Fodder"] -= fodder_eaten


    @staticmethod
    def _island_dict_maker(geo_string):
        geo_string = textwrap.dedent(geo_string)
        geo_list = [list(line) for line in geo_string.splitlines()]
        island_dict = {}

        for i, line in enumerate(geo_list):
            for j, landscape_code in enumerate(line):
                island_dict[(i, j)] = {"Type": landscape_code, "Fodder": 0}

        return island_dict

    @classmethod
    def param_changer(cls, landscape, new_params):
        for key in new_params:
            Island.landscape_parameters[landscape][key] = new_params[key]

