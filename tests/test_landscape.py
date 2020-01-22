
from src.biosim.animals import *
from src.biosim.island import *
from src.biosim.landscape import *
from src.biosim.annual_cycle import *
import pytest


class Test_Landscape:

    def test_landscape_instance(self):
        """Tests if an instance of Landscape can be created.
        """
        land = Landscape()
        assert isinstance(land, Landscape)

    def test_add_pop(self):
        """Tests if an animal can be added to cell.
        """
        herb = Herbivore(Island(), (0,0))
        land = Landscape()
        assert len(land.herb_pop_list) == 0
        land.add_pop(herb)
        assert herb in land.herb_pop_list

    def test_remove_pop(self):
        """Tests if a herbivore and a carnivore can be added
            to and removed from the cell.
        """
        herb = Herbivore(Island(), (0,0))
        carn = Carnivore(Island(), (0,0))
        land = Landscape()
        land.add_pop(herb)
        land.add_pop(carn)
        assert herb in land.herb_pop_list
        assert carn in land.carn_pop_list
        land.remove_pop(herb)
        land.remove_pop(carn)
        assert herb not in land.herb_pop_list
        assert carn not in land.carn_pop_list

    def test_fodder_annual_refill(self):
        """Tests that the fodder refill method can be called.
        """
        land = Landscape()
        land.fodder_annual_refill()

    def test_get_fodder(self):
        """Tests that get fodder method actually retrieves fodder.
        """
        land = Landscape()
        land.fodder = 200
        assert land.get_fodder() == land.fodder

    def test_get_pop_lists(self):
        """Tests that get pop list methods retrieves their
            respective poplists
        """
        land = Landscape()
        land.herb_pop_list.append(Herbivore(Island(), (0,0)))
        land.carn_pop_list.append(Carnivore(Island(), (0,0)))
        assert land.get_herb_pop_list() == land.herb_pop_list
        assert land.get_carn_pop_list() == land.carn_pop_list

    def test_get_num_animals(self):
        """Tests that the number of each animal species can be retrieved using get num animals method.
        """
        land = Landscape()
        num_herb = 3
        num_carn = 2

        for _ in range(num_herb):
            land.add_pop(Herbivore(Island(), (0,0)))

        for _ in range(num_carn):
            land.add_pop(Carnivore(Island(), (0,0)))

        assert land.get_num_herb() == num_herb
        assert land.get_num_carn() == num_carn

    def test_param_changer(self):
        """Tests that the parameters of the landscape can be changed.
        """
        land = Landscape()
        landscape = "J"
        new_param = {"f_max": 700}
        land.param_changer(landscape, new_param)
        assert land.landscape_parameters[landscape]["f_max"] == new_param["f_max"]

    def test_sort_pop_by_fitness(self):
        """Tests that the animal lists in a cell get sorted by fitness when
           sort by fitness method is called
        """
        land = Landscape()
        herb_list = []
        carn_list = []
        for _ in range(3):
            herb = Herbivore(Island(), (0,0))
            carn = Carnivore(Island(), (0,0))
            herb_list.append(herb)
            carn_list.append(carn)
            land.add_pop(herb)
            land.add_pop(carn)

        herb_list.sort(key=lambda herb: herb.fitness, reverse=True)
        carn_list.sort(key=lambda carn: carn.fitness, reverse=True)
        land.sort_pop_by_fitness()

        assert land.get_herb_pop_list() == herb_list
        assert land.get_carn_pop_list() == carn_list

    def test_get_total_herb_weight(self):
        """Tests if get total herb weight method returns weight of 2 herbivores placed in cell.
        """
        land = Landscape()
        assert land.get_total_herb_weight() == 0
        herb_1 = Herbivore(Island(), (0,0))
        land.add_pop(herb_1)
        assert land.get_total_herb_weight() == herb_1.weight
        herb_2 = Herbivore(Island(), (0,0))
        land.add_pop(herb_2)
        assert land.get_total_herb_weight() == herb_1.weight + herb_2.weight

class TestJungle:

    def test_jungle_instance(self):
        """Tests if instance of jungle class can be created.
        """
        j = Jungle()
        assert isinstance(j, Landscape)
        assert isinstance(j, Jungle)

    def test_initial_fodder(self):
        """Tests if initial fodder is set to the max fodder of jungle.
        """
        j = Jungle()
        assert j.get_fodder() == j.landscape_parameters["J"]["f_max"]

    def test_fodder_annual_refill_jungle(self):
        """Tests if fodder annual refill method refills jungle cell to
           max fodder in jungle.
        """
        j = Jungle()
        j.fodder = 400
        j.fodder_annual_refill()
        assert j.get_fodder() == j.landscape_parameters["J"]["f_max"]

    def test_herb_eats_fodder(self):
        """Tests that herb eats fodder method removes same amount of fodder
           as the input value.
        """
        j = Jungle()
        f_max = j.landscape_parameters["J"]["f_max"]
        herb_amount = 10
        j.herb_eats_fodder(herb_amount)
        assert j.get_fodder() == f_max - herb_amount




class TestSavannah:

    def test_savannah_instance(self):
        """Tests if an instance of the Savannah class can be created.
        """
        s = Savannah()
        assert isinstance(s, Landscape)
        assert isinstance(s, Savannah)

    def test_inital_fodder(self):
        """Tests if the initial fodder method gives the cell its max fodder.
        """
        s = Savannah()
        assert s.get_fodder() == s.landscape_parameters["S"]["f_max"]

    def test_fodder_annual_refill_savannah(self):
        """Tests that the fodder annual refill method gives the cell an expected value according to the formula.
        """
        s = Savannah()
        s.fodder = 0
        expected_after_refill = 90
        s.fodder_annual_refill()
        assert s.get_fodder() == expected_after_refill

    def test_savannah_can_not_be_over_max(self):
        """Tests that the fodder annual refill method adjusts the Savannah cells'
           fodder to max would it be above."""
        s = Savannah()
        f_max = s.landscape_parameters["S"]["f_max"]
        s.fodder = f_max + 100
        s.fodder_annual_refill()
        assert s.get_fodder() == f_max

class TestDesert:

    def test_desert_instance(self):
        """Tests that an instance of Desert can be created.
        """
        d = Desert()
        assert isinstance(d, Landscape)
        assert isinstance(d, Desert)


class TestOcean:

    def test_ocean_instance(self):
        """Tests that an instance of Ocean can be created.
        """
        o = Ocean()
        assert isinstance(o, Landscape)
        assert isinstance(o, Ocean)


class TestMountain:

    def test_mountain_instance(self):
        """Tests that an instance of Mountain can be created.
        """
        m = Mountain()
        assert isinstance(m, Landscape)
        assert isinstance(m, Mountain)