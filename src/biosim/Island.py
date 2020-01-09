# -*- coding: utf-8 -*-

class Island:

    def __init__(self, geo_string, params):
        self.island_dict = self._island_dict_maker(geo_string)
        self.params = params

    @staticmethod
    def _island_dict_maker(geo_string):
        geo_list = [list(line) for line in geo_string.splitlines()]
        island_dict = {}

        for i, line in enumerate(geo_list):
            for j, landscape_code in enumerate(line):
                island_dict[(i, j)] = {"Type": landscape_code, "Fodder": 0}

        return island_dict

