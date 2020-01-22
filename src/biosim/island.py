# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov', 'Sigurd Grøtan'
__email__ = 'daniil.vitalevich.efremov@nmbu.no', 'sgrotan@nmbu.no'

import textwrap
from landscape import *
import numpy as np


class Island:
    """SUMMARY
    """

    default_geogr = """\
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

    def __init__(self, geo_string=None):
        """SUMMARY

        :param geo_string: Multi-line string specifying island geography
        :type geo_string: str, optional
        """
        if geo_string is None:
            geo_string = Island.default_geogr
        self._check_geo_string(geo_string)
        self.island_dict = self._island_dict_maker(geo_string)

    def fodder_annual_refill(self):
        """Refills fodder on every location in island
        """
        for loc in self.island_dict:
            self.island_dict[loc].fodder_annual_refill()

    def get_fodder_on_loc(self, loc):
        """Returns fodder on location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: Fodder on input location
        :rtype: float or int
        """
        return self.island_dict[loc].get_fodder()

    def get_herb_list_on_loc(self, loc):
        """Returns the Herbivore list on location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: List of Herbivore on location
        :rtype: list
        """
        return self.island_dict[loc].get_herb_pop_list()

    def get_carn_list_on_loc(self, loc):
        """Returns the Carnivore list on location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: List of Carnivore on location
        :rtype: list
        """
        return self.island_dict[loc].get_carn_pop_list()

    def add_pop_on_loc(self, loc, animal):
        """Adds the input animal-instance of either Herbivore or Carnivore
        class to location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :param animal: An instance of either
        <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        with data and methods, containing info about the animal.
        :type animal: <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        """
        self.island_dict[loc].add_pop(animal)

    def remove_pop_on_loc(self, loc, animal):
        """Removes the input animal-instance of either Herbivore or Carnivore
        class from location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :param animal: An instance of either
        <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        with data and methods, containing info about the animal.
        :type animal: <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        """

        self.island_dict[loc].remove_pop(animal)

    def get_num_herb_on_loc(self, loc):
        """Returns number of Herbivores on location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: Number of Herbivores on loc
        :rtype: int
        """
        return self.island_dict[loc].get_num_herb()

    def get_num_carn_on_loc(self, loc):
        """Returns number of Carnivores on the location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: Number of Carnivores on loc
        :rtype: int
        """
        return self.island_dict[loc].get_num_carn()

    def herb_eats_fodder_on_loc(self, loc, fodder_eaten):
        """Subtracts amount of fodder the Herbivores has eaten from location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :param fodder_eaten: Amount of fodder eaten by Herbivore
        :type fodder_eaten: float
        """
        self.island_dict[loc].herb_eats_fodder(fodder_eaten)

    def sort_all_animals_by_fitness(self):
        """Sorts all animals in island by fitness.
        """
        for loc in self.island_dict:
            self.island_dict[loc].sort_pop_by_fitness()

    def get_all_herb_list(self):
        """Returns list containing all Herbivores on island

        :return: List with all Herbivores
        :rtype: list
        """
        all_herb_list = []
        for loc in self.island_dict:
            all_herb_list.extend(self.get_herb_list_on_loc(loc))
        return all_herb_list

    def get_all_carn_list(self):
        """Returns list containing all Carnivores on island

        :return: List with all Carnivores
        :rtype: list
        """
        all_carn_list = []
        for loc in self.island_dict:
            all_carn_list.extend(self.get_carn_list_on_loc(loc))
        return all_carn_list

    def get_total_herb_weight_on_loc(self, loc):
        """Returns the total Herbivore weight on location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: Total Herbivore weight on loc
        :rtype: float
        """
        return self.island_dict[loc].get_total_herb_weight()

    def get_cell_type(self, loc):
        """Returns cell type on location

        :param loc: Indicates the coordinates in island
        :type loc: tuple
        :return: Cell type
        :rtype: str
        """
        return self.island_dict[loc].__class__.__name__

    @staticmethod
    def _check_geo_string(geo_string):
        """ Checks if the geo_string is of correct shape, and if the edges of
        the map is of Ocean type. Raises value error if not.

        :param geo_string: Multi-line string specifying island geography
        :type geo_string: str
        :raises ValueError: If map is not of rectangular shape
        :raises ValueError: If the edges of the map are not Ocean type
        """
        geo_string = textwrap.dedent(geo_string)
        geo_list = [list(line) for line in geo_string.splitlines()]
        for line in geo_list:
            if len(line) != len(geo_list[0]):
                raise ValueError("The map string has to be of rectangular shape!")

        geo_matrix = np.array(geo_list)
        top_slice = geo_matrix[0, :]
        bottom_slice = geo_matrix[-1, :]
        left_slice = geo_matrix[:, 0]
        right_slice = geo_matrix[:, -1]
        whole_frame_array = np.concatenate((top_slice, bottom_slice, left_slice, right_slice), axis=None)

        for geo in whole_frame_array:
            if geo != "O":
                raise ValueError("The edges of the map must be all ocean type!")

    @property
    def island_data(self):
        """Returns a nested list containing x coordinate, y coordinate,
        Herbivore-count on loc and Carnivore-count on loc

        :return: Nested list with data
        :rtype: list
        """
        island_data = []
        for loc in self.island_dict:
            i, j = loc[0], loc[1]
            herb_count = self.get_num_herb_on_loc(loc)
            carn_count = self.get_num_carn_on_loc(loc)
            island_data.append([i, j, herb_count, carn_count])
        return island_data



    @staticmethod
    def _island_dict_maker(geo_string):
        """Turns geo_string into a readable format and creates a dictionary
        containing x, y coordinates as key, and an instance of one of the five
        landscape subclasses as value.

        :param geo_string: Multi-line string specifying island geography
        :type geo_string: str
        :raise ValueError: If geo_string does not contain correct letters
        :return: Dict with location as key, and instance of landscape subclass
        as value
        :rtype: dict
        """
        geo_string = textwrap.dedent(geo_string)
        geo_list = [list(line) for line in geo_string.splitlines()]
        island_dict = {}

        for i, line in enumerate(geo_list):
            for j, landscape_code in enumerate(line):
                landscape_code = landscape_code.upper()
                if landscape_code == "O":
                    geo = Ocean()
                elif landscape_code == "J":
                    geo = Jungle()
                elif landscape_code == "M":
                    geo = Mountain()
                elif landscape_code == "S":
                    geo = Savannah()
                elif landscape_code == "D":
                    geo = Desert()
                else:
                    raise ValueError("Geography string must consist of only O, J, M, S, D")
                island_dict[(i, j)] = geo

        return island_dict

    @staticmethod
    def _param_changer(landscape, new_params):
        """Calls on param_changer method from Landscape-class to change
        parameters used to created the Landscape cells in the island map.

        :param landscape: One letter string containing the landscape_code
        for either Jungle or Savannah.
        :type landscape: str
        :param new_params: dictionary containing the parameters to change
        :type new_params: dict
        :raise ValueError: If the parameter does not exist in default-list
        :raise ValueError: If one of the parameters that are not supposed to
        be a negative number, gets set to a negative number
        """

        params_non_negative = ["f_max"]
        for key in new_params:
            if key not in Landscape.landscape_parameters[landscape]:
                raise ValueError("Can not change parameter "
                                 "'{0}' since the parameter does "
                                 "not exist in default-list".format(key))

            if key in params_non_negative and new_params[key] < 0:
                raise ValueError("Parameter {0} must be a nonnegative value."
                                 .format(key))

        Landscape.param_changer(landscape, new_params)

    @property
    def locations(self):
        return set(self.island_dict.keys())



