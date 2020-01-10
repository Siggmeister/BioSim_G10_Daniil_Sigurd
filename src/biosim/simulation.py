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

        self.landscape_parameters = {"J": {"f_max": 800.0},
                                     "S": {"f_max": 300.0,
                                           "alpha": 0.3}}

        self.animal_parameters = {"Herbivore":  {"w_birth": 8.0,
                                                 "sigma_birth": 1.5,
                                                 "beta": 0.9,
                                                 "eta": 0.05,
                                                 "a_half": 40.0,
                                                 "phi_age": 0.2,
                                                 "w_half": 10.0,
                                                 "phi_weight": 0.1,
                                                 "mu": 0.25,
                                                 "lambda": 1.0,
                                                 "gamma": 0.2,
                                                 "zeta": 3.5,
                                                 "xi": 1.2,
                                                 "omega": 0.4,
                                                 "F": 10.0}}
        self.island = island.Island(island_map, self.landscape_parameters)
        self.herb_list = self.ini_pop_maker(ini_pop, self.island)
        self.carn_list = []

    def ini_pop_maker(self, animal_spec_list, island):
        herb_pop_list = []
        for loc_dict in animal_spec_list:
            for animal in loc_dict["pop"]:
                a = animals.Herbivore(island=island, parameters=self.animal_parameters["Herbivore"],
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
        for key in params:
            self.animal_parameters[species][key] = params[key]

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        for key in params:
            self.landscape_parameters[landscape][key] = params[key]

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
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(79)
            ],
        }
    ]

    s = BioSim(geogr, ini_herbs)
    print(s.island.island_dict[(10, 10)]["Fodder"])
    s.simulate(5)
    print(s.island.island_dict[(10, 10)]["Fodder"])
    #s.island.fodder_annual_refill()
    print(s.island.island_dict[(10, 10)]["Fodder"])
    print(len(s.herb_list))

    print(s.island.island_dict[(10,10)]["Type"])