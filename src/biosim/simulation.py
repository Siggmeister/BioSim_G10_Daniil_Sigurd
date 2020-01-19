# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

from island import *
from animals import *
from annual_cycle import *

class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed=None,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """

        self.island = Island(island_map)
        self.add_population(ini_pop)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == "Herbivore":
            Herbivore.param_changer(params)
        elif species == "Carnivore":
            Carnivore.param_changer(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        self.island._param_changer(landscape, params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        cycle = AnnualCycle(self.island)
        cycle.run_cycle(num_years)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

        for loc_dict in population:
            loc = loc_dict["loc"]
            cell_type = self.island.get_cell_type(loc)
            if cell_type == "Ocean" or cell_type == "Mountain":
                raise ValueError("Animal can not be placed in mountain or ocean!")

            for animal_dict in loc_dict["pop"]:
                age = animal_dict["age"]
                weight = animal_dict["weight"]

                if animal_dict["species"] == "Herbivore":
                    Herbivore(self.island, loc, age, weight)
                elif animal_dict["species"] == "Carnivore":
                    Carnivore(self.island, loc, age, weight)

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

if __name__ == '__main__':
    geogr = """\
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

    ini_herbs = [
        {
            "loc": (2, 7),
            "pop": [
                {"species": "Herbivore", "age": 45, "weight": 200}
                for _ in range(150)
            ],
        },

    ]

    carn_pop = [{
            "loc": (2, 7),
            "pop": [
                {"species": "Carnivore", "age": 55, "weight": 20}
                for _ in range(20)
            ],
        }]

    s = BioSim(geogr, ini_herbs)
    s.set_landscape_parameters("J", {"f_max": 700})
    for _ in range(100):
        s.simulate(1)
        print(len(s.island.get_all_herb_list()))
        print("-----------------")
        print(len(s.island.get_all_carn_list()))
        print("")
    s.add_population(carn_pop)
    for _ in range(200):
        s.simulate(1)
        print(len(s.island.get_all_herb_list()))
        print("-----------------")
        print(len(s.island.get_all_carn_list()))
        print("")
    print(s.island.island_dict[(2,7)].__class__.__name__)
    print("======================")
    #print(s.island.get_all_herb_list()[0].fitness, s.island.get_all_herb_list()[0].weight)
    #print(s.island.get_all_carn_list()[0].fitness, s.island.get_all_carn_list()[0].weight)
