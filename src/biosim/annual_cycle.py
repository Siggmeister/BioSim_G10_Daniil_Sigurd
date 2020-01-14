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

    def sort_by_fitness(self):
        self.herb_pop_list.sort(key=lambda herb: herb.fitness, reverse=True)
        self.carn_pop_list.sort(key=lambda carn: carn.fitness, reverse=True)

    def herb_feeding(self):
        for herb in self.herb_pop_list:
            herb.feed()

    def carn_feeding(self):
        pass

    def procreation_herb(self):
        for herb in self.herb_pop_list:
            herb.birth(self.herb_pop_list)

    def procreation_carn(self):
        for carn in self.carn_pop_list:
            carn.birth(self.carn_pop_list)

    def procreation_all(self):
        self.procreation_herb()
        self.procreation_carn()

    def aging(self):
        for animal in self.herb_pop_list + self.carn_pop_list:
            animal.aging()

    def weight_loss(self):
        for animal in self.herb_pop_list + self.carn_pop_list:
            animal.annual_weight_loss()

    def animal_death(self):
        for animal in self.herb_pop_list + self.carn_pop_list:
            if animal.death():
                self.herb_pop_list.remove(animal)
                self.island.remove_pop_on_loc(animal.get_loc(), animal)

    def cycle(self, num_years):
        for _ in range(num_years):
            self.fodder_growth()
            self.sort_by_fitness()
            self.herb_feeding()
            self.carn_feeding()
            self.procreation_all()
            self.aging()
            self.weight_loss()
            self.animal_death()
            self.num_cycles += 1
