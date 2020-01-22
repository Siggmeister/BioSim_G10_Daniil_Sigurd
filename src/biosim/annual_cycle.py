# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'


class AnnualCycle:
    """Annual cycle class. Manages all the yearly events on the island.
    """

    def __init__(self, island):
        """Annual cycle class. Manages all the yearly events on the island.

        :param island: An instance of the :class:'src.biosim.island.Island'
        with data and methods, containing info about the geography.
        :type island: class:'src.biosim.island.Island'
        """
        self.island = island

    def fodder_growth(self):
        """Refills fodder depending on Landscape-type.
        """
        self.island.fodder_annual_refill()

    def sort_by_fitness(self):
        """Sorts all animals by fitness
        """
        self.island.sort_all_animals_by_fitness()

    def herb_feeding(self):
        """Feeds all Herbivores in Island
        """
        all_herb = self.island.get_all_herb_list()
        for herb in all_herb:
            herb.feed()

    def carn_feeding(self):
        """Feeds all Carnivores in Island
        """
        all_carn = self.island.get_all_carn_list()
        for carn in all_carn:
            carn.feed()

    def procreation_herb(self):
        """Gives birth to Herbivores
        """
        all_herb = self.island.get_all_herb_list()
        for herb in all_herb:
            herb.birth()

    def procreation_carn(self):
        """Gives birth to Carnivores
        """
        all_carn = self.island.get_all_carn_list()
        for carn in all_carn:
            carn.birth()

    def procreation_all(self):
        """Gives birth to both Carnivores and Herbivores
        """
        self.procreation_herb()
        self.procreation_carn()

    def aging(self):
        """Adds a year to all Herbivores and Carnivores
        and redefines their fitness.
        """
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            animal.aging()

    def weight_loss(self):
        """Makes all Herbivores and Carnivores loose annual weight
        """
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            animal.annual_weight_loss()

    def animal_death(self):
        """Removes dead Herbivores and Carnivores from Island
        """
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            if animal.death():
                self.island.remove_pop_on_loc(animal.get_loc(), animal)

    def migration(self):
        """Makes Herbivores and Carnivores migrate if needed
        """
        all_herb = self.island.get_all_herb_list()
        all_carn = self.island.get_all_carn_list()
        for animal in all_herb + all_carn:
            animal.migrate()

    def run_cycle(self):
        """Calls on all of the methods in the AnnualCycle class
        in the right order of the cycle.
        """
        self.fodder_growth()
        self.sort_by_fitness()
        self.herb_feeding()
        self.carn_feeding()
        self.procreation_all()
        self.migration()
        self.aging()
        self.weight_loss()
        self.animal_death()
