# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'


class AnnualCycle:
    param_dict_jungle = {"f_max": 800}
    param_dict_savannah = {"f_max": 300, "alpha": 0.3}

    def __init__(self, herb_list, carn_list, island_dict):
        pass

    #    def fodder_growth(self, island_dict):
    #
    #        max_jungle_fodder = 800
    #        max_savannah_fodder = 300
    #        alpha = 0.3
    #
    #        for key in island_dict:
    #            if island_dict[key]["Type"] == "J":
    #                island_dict[key]["Fodder"] = max_jungle_fodder
    #
    #            if island_dict[key]["Type"] == "S":
    #                island_dict[key]["Fodder"] += (alpha *
    #                (max_savannah_fodder-island_dict[key]["Fodder"]))

    #    def fodder_growth_jungle(self, parameters = None, island_dict):
    #        if parameters is None:
    #            parameters = AnnualCycle.param_dict_jungle
    #
    #
    #        for key in island_dict:
    #            island_dict[key]["Fodder"] = max_jungle_fodder
    #
    #    def fodder_growth_savannah(self, parameters = None, island_dict):
    #        if parameters is None:
    #            parameters = AnnualCycle.param_dict_savannah
    #        self.parameters = parameters
    #
    #        for key in island_dict:
    #            island_dict[key]["Fodder"] += (alpha *
    #                (self.parameters[]-island_dict[key]["Fodder"])) #Endre
    #
    #

    def herb_feeding(self):
        pass

    def carn_feeding(self):
        pass

    def procreation(self):
        pass

    def aging(self):
        pass

    def weight_loss(self):
        pass

    def animal_death(self):
        pass

