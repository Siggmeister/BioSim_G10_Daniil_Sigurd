# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'


class AnnualCycle:

    def __init__(self, herb_pop_list, carn_pop_list, island):
        self.herb_pop_list = herb_pop_list
        self.carn_pop_list = carn_pop_list
        self.island = island
        self.num_cycles = 0

    def fodder_growth(self):
        self.island.fodder_annual_refill()

    def herb_feeding(self):
        for herb in self.herb_pop_list:
            herb.feed()

    def carn_feeding(self):
        pass

    def procreation(self):
        for herb in self.herb_pop_list:
            herb.birth(self.herb_pop_list)

    def aging(self):
        for herb in self.herb_pop_list:
            herb.aging()

    def weight_loss(self):
        for herb in self.herb_pop_list:
            herb.annual_weight_loss()

    def animal_death(self):
        for herb in self.herb_pop_list:
            if herb.death():
                self.herb_pop_list.remove(herb)

    def cycle(self, num_years):
        for _ in range(num_years):
            self.fodder_growth()
            self.herb_feeding()
            self.carn_feeding()
            self.procreation()
            self.aging()
            self.weight_loss()
            self.animal_death()
            self.num_cycles += 1
