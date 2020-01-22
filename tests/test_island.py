# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from src.biosim.island import *
from animals import *
from src.biosim.landscape import *
import pytest


class TestIsland:

    def test_island_instance(self):
        """Tests if an instance of Island can be created.
        """
        i = Island()
        assert isinstance(i, Island)

    def test_check_geo_string_not_surrounded_by_ocean(self):
        """Tests that check geo string method raises ValueError if
           the string is not surrounded by Ocean code.
           """
        geo_string_1 = """\
                    OOOOOOOOOOOO
                    OOOJJSSSSMMM
                    OSSSSSJJJJMM
                    """
        with pytest.raises(ValueError):
            Island._check_geo_string(geo_string_1)

    def test_check_geo_string_not_rectangular(self):
        """Tests that the geo string checker raises ValueError if the geo string
           is non-rectangular
        """

        geo_string_2 = """\
                    OOOOOOOOOOOO
                    OOOJJSSSSMMOOO
                    OOOOOOOOOOOOOOOO
                    """
        with pytest.raises(ValueError):
            Island._check_geo_string(geo_string_2)

    def test_geo_string_works_with_upper_and_lower_case(self):
        """Test that the island dict maker method passes when geo string is both
           lower and upper case.
        """
        geo_string = """\
                    OOOOOOOOoOOO
                    OOOJJSSSsMMO
                    OSSSsSJjJJMO
                    OOOoOOOOoooO
                    """
        island_dict = Island._island_dict_maker(geo_string)

    def test_geo_string_with_wrong_code_letters(self):
        """Test that island dict maker raises ValueError when it detects unknown landscape
           code.
           """
        geo_string = """\
                            OOOO
                            OSLO
                            OOOO
                            """
        with pytest.raises(ValueError):
            Island._island_dict_maker(geo_string)

    def test_fodder_annual_refill(self):
        """Tests that fodder annual refill method raises the fodder in all Jungle and Savannah
           cells.
           """
        i = Island()
        for loc in i.island_dict:
            i.island_dict[loc].fodder = 0
        i.fodder_annual_refill()
        for loc in i.island_dict:
            loc_type = i.island_dict[loc].__class__.__name__
            loc_fodder = i.island_dict[loc].fodder
            if loc_type == "Jungle" or loc_type == "Savannah":
                assert loc_fodder > 0
            else:
                assert loc_fodder == 0

    def test_get_fodder_on_loc(self):
        """Tests if get fodder on loc method retrieves fodder attribute of cell on location.
        """
        i = Island()
        j_loc = (2, 7)
        fodder_on_loc = i.island_dict[j_loc].fodder
        assert i.get_fodder_on_loc(j_loc) == fodder_on_loc

    def test_get_herb_list_on_loc(self):
        """Tests if get herb list on loc method retrieves herb list attribute of
           cell on locatrion.
           """
        i = Island()
        loc = (1, 8)
        for _ in range(3):
            Herbivore(i, loc)

        herb_list_manually = i.island_dict[loc].herb_pop_list
        assert i.get_herb_list_on_loc(loc) == herb_list_manually

    def test_get_carn_list_on_loc(self):
        """Tests if get carn list on loc method retrieves carn list attribute of
        cell on locatrion.
        """
        i = Island()
        loc = (1, 8)
        for _ in range(3):
            Carnivore(i, loc)

        carn_list_manually = i.island_dict[loc].carn_pop_list
        assert i.get_carn_list_on_loc(loc) == carn_list_manually

    def test_add_and_remove_pop_on_locs(self):
        """Tests if the add and remove pop on loc methods can add and remove a sample of animals
           in the pop lists.
        """
        i = Island()
        loc_1 = (1, 8)
        loc_2 = (2, 7)
        animal_list = [Herbivore(i, loc_1), Carnivore(i, loc_1)]
        for animal in animal_list:
            new_cell = i.island_dict[loc_2]
            old_cell = i.island_dict[loc_1]
            i.add_pop_on_loc(loc_2, animal)
            i.remove_pop_on_loc(loc_1, animal)
            if animal.__class__.__name__ == "Herbivore":
                assert animal in new_cell.herb_pop_list
                assert animal not in old_cell.herb_pop_list
            elif animal.__class__.__name__ == "Carnivore":
                assert animal in new_cell.carn_pop_list
                assert animal not in old_cell.carn_pop_list

    def test_get_num_animals_on_loc(self):
        """Tests if the get animals on location method can return the number
           of animals placed out on the map.
           """
        i = Island()
        num_herb = 4
        num_carn = 3
        loc = (2, 7)
        for _ in range(num_herb):
            Herbivore(i, loc)
        for _ in range(num_carn):
            Carnivore(i, loc)

        assert i.get_num_herb_on_loc(loc) == num_herb
        assert i.get_num_carn_on_loc(loc) == num_carn

    def test_sort_all_animals_by_fitness(self):
        """Tests if the sort all animals by fitness method sorts a sample of animals placed
           on a location by fitness.
           """
        i = Island()
        loc = (2, 7)
        for _ in range(10):
            Herbivore(i, loc)
            Carnivore(i, loc)

        local_herb_list = i.get_herb_list_on_loc(loc)
        local_carn_list = i.get_carn_list_on_loc(loc)
        local_herb_list.sort(key=lambda herb: herb.fitness, reverse=True)
        local_carn_list.sort(key=lambda carn: carn.fitness, reverse=True)

        i.sort_all_animals_by_fitness()

        assert i.get_herb_list_on_loc(loc) == local_herb_list
        assert i.get_carn_list_on_loc(loc) == local_carn_list

    def test_get_total_herb_weight_on_loc(self):
        """Tests if the get total herbivore weight on location method returns the same
           weight as the weight of the herbivores times their number.
           """
        i = Island()
        herb_weight = 50
        num_herb = 5
        loc = (2, 7)
        for _ in range(num_herb):
            Herbivore(i, loc, weight=herb_weight)

        assert i.get_total_herb_weight_on_loc(loc) == herb_weight * num_herb

    def test_get_cell_type(self):
        """Tests if the get cell type method returns Jungle on a known
           jungle location.
           """
        i = Island()
        jungle_loc = (2, 7)
        assert i.get_cell_type(jungle_loc) == "Jungle"

    def test_herb_eats_fodder_on_loc(self):
        """Tests if the fodder before eating is equal to the fodder after eating
           in addition to the amount eaten.
        """
        i = Island()
        j_loc = (2, 7)
        herb_amount = 10
        fodder_pre_eating = i.island_dict[j_loc].fodder
        i.herb_eats_fodder_on_loc(j_loc, herb_amount)
        fodder_post_eating = i.island_dict[j_loc].fodder
        assert fodder_pre_eating == fodder_post_eating + herb_amount

    def test_get_all_herb_list(self):
        """Tests that the get all herbivores list method returns a list that is equal in length
           and contains the same elements as a list containing all the herbivores on the map.
           """
        i = Island()
        herb_list = [Herbivore(i, (2, 7)), Herbivore(i, (1, 8)), Herbivore(i, (2, 1))]
        all_herbs = i.get_all_herb_list()
        assert len(all_herbs) == len(herb_list)
        for herb in herb_list:
            assert herb in all_herbs

    def test_get_all_carn_list(self):
        """Tests that the get all carnivores list method returns a list that is equal in length
           and contains the same elements as a list containing all the carnivores on the map.
        """
        i = Island()
        carn_list = [Carnivore(i, (2, 7)), Carnivore(i, (1, 8)), Carnivore(i, (2, 1))]
        all_carns = i.get_all_carn_list()
        assert len(all_carns) == len(carn_list)
        for carn in carn_list:
            assert carn in all_carns

    def test_param_changer(self):
        """Tests that the parameter changer method in the Island class changes the parameters in
           the Landscape class.
        """
        i = Island()
        new_param = {"f_max": 700}
        landscape = "J"
        i._param_changer(landscape, new_param)
        assert i.island_dict[(0, 0)].landscape_parameters[landscape]["f_max"] == 700



