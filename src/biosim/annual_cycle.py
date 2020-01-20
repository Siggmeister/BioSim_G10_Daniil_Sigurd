# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'


class AnnualCycle:

    def __init__(self, island):
        self.island = island
        #self.num_cycles = 0

    def fodder_growth(self):
        self.island.fodder_annual_refill()

    def sort_by_fitness(self):
        self.island.sort_all_animals_by_fitness()

    def herb_feeding(self):
        all_herb = self.island.get_all_herb_list()
        for herb in all_herb:
            herb.feed()

    def carn_feeding(self):
        all_carn = self.island.get_all_carn_list()
        for carn in all_carn:
            carn.feed()

    def procreation_herb(self):
        all_herb = self.island.get_all_herb_list()
        for herb in all_herb:
            herb.birth()

    def procreation_carn(self):
        all_carn = self.island.get_all_carn_list()
        for carn in all_carn:
            carn.birth()

    def procreation_all(self):
        self.procreation_herb()
        self.procreation_carn()

    def aging(self):
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            animal.aging()

    def weight_loss(self):
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            animal.annual_weight_loss()

    def animal_death(self):
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            if animal.death():
                self.island.remove_pop_on_loc(animal.get_loc(), animal)

    def migration(self):
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            animal.migrate()

    def run_cycle(self):
        self.fodder_growth()
        self.sort_by_fitness()
        self.herb_feeding()
        self.carn_feeding()
        self.procreation_all()
        self.migration()
        self.aging()
        self.weight_loss()
        self.animal_death()
