# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import island
import animals
import annual_cycle

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

        self.island = island.Island(island_map)
        self.herb_list = self.ini_pop_maker(ini_pop, self.island)
        self.carn_list = []

    def ini_pop_maker(self, animal_spec_list, island):
        herb_pop_list = []
        for loc_dict in animal_spec_list:
            for animal in loc_dict["pop"]:
                a = animals.Herbivore(island=island,
                                   loc=loc_dict["loc"],
                                   age=animal["age"],
                                   weight=animal["weight"])
                herb_pop_list.append(a)
        return herb_pop_list



    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        animals.Animals.param_changer(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        island.Island.param_changer(landscape, params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        Cycle = annual_cycle.AnnualCycle(self.herb_list, [], self.island)
        Cycle.cycle(num_years)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

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
            "loc": (6, 8),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 50}
                for _ in range(10)
            ],
        }
    ]

    s = BioSim(geogr, ini_herbs)
    for _ in range(1):
        s.simulate(1)
        print(len(s.herb_list))
        print(s.island.get_herb_list_on_loc((6,8)))
    print(s.island.island_dict[(6,8)].__class__.__name__)
    print("------------")
    print(len(s.herb_list))
    print(s.island.get_num_herb_on_loc((6,8)))
