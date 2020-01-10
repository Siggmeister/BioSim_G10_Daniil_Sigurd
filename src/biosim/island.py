# -*- coding: utf-8 -*-

class Island:

    def __init__(self, geo_string, params):
        self.island_dict = self._island_dict_maker(geo_string)
        self.params = params
        self.initial_fodder()

    def initial_fodder(self):
        f_max_jungle = self.params["J"]["f_max"]
        f_max_savannah = self.params["S"]["f_max"]

        for loc in self.island_dict:
            geo_type = self.island_dict[loc]["Type"]
            if geo_type == "J":
                self.island_dict[loc]["Fodder"] = f_max_jungle
            elif geo_type == "S":
                self.island_dict[loc]["Fodder"] = f_max_savannah

    def fodder_annual_refill(self):
        f_max_jungle = self.params["J"]["f_max"]
        f_max_savannah = self.params["S"]["f_max"]
        alpha = self.params["S"]["alpha"]

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
        geo_list = [list(line) for line in geo_string.splitlines()]
        island_dict = {}

        for i, line in enumerate(geo_list):
            for j, landscape_code in enumerate(line):
                island_dict[(i, j)] = {"Type": landscape_code, "Fodder": 0}

        return island_dict


