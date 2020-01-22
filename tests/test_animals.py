# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov', 'Sigurd Grøtan'
__email__ = 'daniil.vitalevich.efremov@nmbu.no', 'sgrotan@nmbu.no'

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.island import Island
import pytest
from mock import patch



class TestAnimals:

    @pytest.fixture(autouse=True)
    def setup(self):
        spes_geogr_1 = """\
                       OOOO
                       OOJO
                       OOOO"""

        self.spes_geogr_2 = """\
                               OOOO
                               OJJO
                               OOOO"""
        self.spes_island = Island(spes_geogr_1)
        self.i = Island()
        self.loc = (0,0)
        stnd_herb = Herbivore(island=self.i, loc=self.loc)
        stnd_carn = Carnivore(island=self.i, loc=self.loc)
        self.stnd_a_list = [stnd_herb, stnd_carn]

        self.herb_w_0 = Herbivore(island=self.i, loc=self.loc, weight = 0)
        self.herb_w_5 = Herbivore(island=self.i, loc=self.loc, weight = 5)
        self.herb_w_200 = Herbivore(island=self.i, loc=self.loc, weight=200)

        self.carn_w_0 = Carnivore(island=self.i, loc=self.loc, weight=0)
        self.carn_w_5 = Carnivore(island=self.i, loc=self.loc, weight=5)
        self.carn_w_7 = Carnivore(island=self.i, loc=self.loc, weight=7)

        self.a_list_w_0 = [self.herb_w_0, self.carn_w_0]
        self.a_list_w_5 = [self.herb_w_5, self.carn_w_5]

    def test_get_params_herb(self):
        """Manual test on collecting parameter key/value for Herbivore
        """
        assert Herbivore.parameters["beta"] == 0.9
        assert Herbivore.parameters["a_half"] == 40.0
        assert Herbivore.parameters["lambda"] == 1.0
        assert Herbivore.parameters["F"] == 10.0

    def test_get_params_carn(self):
        """Manual test on collecting parameter key/value for Carnivore
        """
        assert Carnivore.parameters["beta"] == 0.75
        assert Carnivore.parameters["a_half"] == 60.0
        assert Carnivore.parameters["lambda"] == 1.0
        assert Carnivore.parameters["F"] == 50.0

    def test_aging(self):
        """Test if the age of all animals increase by
        1 for each time method is called
        """
        for a in self.stnd_a_list:
            a.aging()

            assert a.age == 1
            a.age = 0

            for _ in range(5):
                a.aging()

            assert a.age == 5

    def test_get_loc_returns_loc(self):
        """Test get_loc returns location
        """
        for a in self.stnd_a_list:

            assert a.get_loc() == self.loc

    def test_get_fitness_returns_fitness(self):
        """Test get_fitness returns fitness
        """
        for a in self.a_list_w_0:
            assert a.get_fitness() == 0

        assert self.herb_w_5.get_fitness() == pytest.approx(0.377, 0.01)
        assert self.carn_w_5.get_fitness() == pytest.approx(0.598, 0.01)

    def test_param_changer_changes(self):
        """Test param_changer changes the parameter list
        """
        i = Island()
        loc = (1, 1)
        s = Herbivore(i, loc)
        old_param = s.parameters["F"]
        s.param_changer({"F" : 20})
        new_param = s.parameters["F"]

        assert old_param != new_param
        s.param_changer({"F": 10})

    def test_fitness_change_for_set_weight(self):
        """Manual test for fitness_change on set weight
        """
        self.herb_w_5.fitness_change()
        self.herb_w_200.fitness_change()
        self.carn_w_5.fitness_change()
        self.carn_w_7.fitness_change()
        self.herb_w_0.fitness_change()
        self.carn_w_0.fitness_change()

        assert self.herb_w_5.fitness == pytest.approx(0.377, 0.01)
        assert self.herb_w_200.fitness == pytest.approx(0.998, 0.01)
        assert self.carn_w_5.fitness == pytest.approx(0.598, 0.01)
        assert self.carn_w_7.fitness == pytest.approx(0.768, 0.01)
        assert self.herb_w_0.fitness == 0
        assert self.carn_w_0.fitness == 0

    def test_weight_gain(self):
        """Test weight_gains according to formula
        """
        fodder_eaten = Herbivore.parameters["F"]
        beta = Herbivore.parameters["beta"]
        self.herb_w_5.weight_gain(fodder_eaten)

        assert self.herb_w_5.weight == 5+(fodder_eaten*beta)

    def test_feed_changes_fitness(self):
        """Test feed changes fitness
        """
        loc = (2,1)
        i = Island()
        i_sim = Herbivore(i, loc)
        start_fitness = i_sim.fitness
        i_sim.feed()
        changed_fitness = i_sim.fitness

        assert start_fitness != changed_fitness


    def test_can_birth_occur_with_1_herbivore(self):
        """Test to see that birth will not occur for only 1 animal
        """
        loc = (2,7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc)
        i_sim.add_pop_on_loc(loc, a_sim)

        assert not a_sim.can_birth_occur()

    def test_can_birth_occur_with_2_herbivores_with_1_prob(self, mocker):
        """Test to show that 2 herbivores will give birth if the probability 
        is mocked to the lowest possible value.
        """
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight = 100)
        for _ in range(2):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert a_sim.can_birth_occur()

    def test_can_birth_occur_with_2_carnivores_with_1_prob(self, mocker):
        """Test to show that 2 carnivores will give birth if the probability
        is mocked to the lowest possible value.
        """
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Carnivore(i_sim, loc, weight=100)
        for _ in range(2):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert a_sim.can_birth_occur()

    def test_can_birth_occur_with_2_herbivores_with_0_prob(self, mocker):
        """Test to show that 2 herbivores will not give birth if the
        probability is mocked to highest possible value.
        """
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        a_sim = Herbivore(i_sim, loc, weight=100)
        for _ in range(2):
            i_sim.add_pop_on_loc(loc, a_sim)

        assert not a_sim.can_birth_occur()

    def test_birth_adds_to_num_herb_on_loc(self, mocker):
        """Test to show that birth method adds new pop to herb_pop list
         when birth occurs
         """
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim_1 = Herbivore(i_sim, loc, weight=100)
        a_sim_2 = Herbivore(i_sim, loc, weight=100)

        a_sim_1.birth()

        assert i_sim.get_num_herb_on_loc(loc) == 3

    def test_birth_adds_to_num_carn_on_loc(self, mocker):
        """Test to show that birth method adds new pop to carn_pop list
        when birth occurs
        """
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        a_sim_1 = Carnivore(i_sim, loc, weight=100)
        a_sim_2 = Carnivore(i_sim, loc, weight=100)

        a_sim_1.birth()

        assert i_sim.get_num_carn_on_loc(loc) == 3

    def test_birth_does_not_happen_if_prob_0(self, mocker):
        """Test to show that birth method does not add new pop if
        birth does not occur
        """
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        a_sim_1 = Herbivore(i_sim, loc, weight=100)
        a_sim_2 = Herbivore(i_sim, loc, weight=100)

        a_sim_1.birth()

        assert i_sim.get_num_herb_on_loc(loc) == 2

    @patch.object(Herbivore, 'can_birth_occur')
    def test_birth_does_not_add_new_baby_if_weight_too_low(self, mocker):
        """Test to show that if birth weight is too low, a new baby will not
        be born"""
        a_sim_1 = Herbivore(self.i, self.loc, weight=1)
        mocker.return_value = True
        a_sim_2 = Herbivore(self.i, self.loc, weight=1)
        old_pop = a_sim_1.get_num_same_species(self.loc)
        a_sim_1.birth()
        new_pop = a_sim_1.get_num_same_species(self.loc)

        assert old_pop == new_pop

    def test_annual_weight_loss_decreases_weight(self):
        """Test to show that annual_weight_loss decreases the
        weight of the animal
        """
        loc = (2,7)
        i = Island()
        a_sim = Herbivore(i, loc)
        initial_weight = a_sim.weight
        a_sim.annual_weight_loss()
        new_weight = a_sim.weight

        assert initial_weight > new_weight

    def test_death_occurs_if_fitness_is_0(self):
        """Test to show that animal will die if fitness is 0
        """
        loc = (2, 7)
        i = Island()
        h_sim = Herbivore(i, loc, weight=0)
        c_sim = Carnivore(i, loc, weight=0)


        assert h_sim.death()
        assert c_sim.death()

    def test_death_occurs_if_prob_is_1(self, mocker):
        """Test to show that death will occur if we mock the probability to
        lowest return value
        """
        mocker.patch('random.random', return_value=0)
        loc = (2, 7)
        i_sim = Island()
        h_sim = Herbivore(i_sim, loc)
        c_sim = Carnivore(i_sim, loc)

        assert h_sim.death()
        assert c_sim.death()

    def test_death_does_not_occur_if_prob_is_0(self, mocker):
        """Test to show that death will not occur if we mock the probability to
        highest return value
        """
        mocker.patch('random.random', return_value=1)
        loc = (2, 7)
        i_sim = Island()
        h_sim = Herbivore(i_sim, loc)
        c_sim = Carnivore(i_sim, loc)

        assert not h_sim.death()
        assert not c_sim.death()

    def test_will_move_does_not_happen_if_prob_0(self, mocker):
        """Test to show that move will not happen if we mock the probability
        to highest value
        """
        mocker.patch('random.random', return_value=1)
        a_sim = Herbivore(self.i, self.loc)

        assert not a_sim.will_move()

    def test_will_move_happens_if_prob_1(self, mocker):
        """Test to show that move will happen if we mock the probability
        to lowest value
        """
        mocker.patch('random.random', return_value=0)
        a_sim = Herbivore(self.i, self.loc)

        assert a_sim.will_move()

    def test_get_relevant_fodder_herb(self):
        """Test to show that get_relevant_fodder returns fodder for herb
        """
        jungle_loc = (2,7)
        a = Herbivore(self.i, jungle_loc)
        fodder = self.i.get_fodder_on_loc(jungle_loc)

        assert a.get_relevant_fodder(jungle_loc) == fodder

    def test_get_relevant_fodder_carn(self):
        """Test to show that get_relevant_fodder returns fodder for carn,
        which is equal to the herb_weight
        """
        i = Island()
        c = Carnivore(i, self.loc)
        herb_weight = 50
        h = Herbivore(i, self.loc, weight=herb_weight)

        assert c.get_relevant_fodder(self.loc) == herb_weight

    def test_get_num_same_species_herb(self):
        """Test to show that get_num_same_species
        return is number of same species(herb)
        """
        i = Island()
        h_1 = Herbivore(i, self.loc)
        h_2 = Herbivore(i, self.loc)

        assert h_1.get_num_same_species(self.loc) == 2

    def test_get_num_same_species_carn(self):
        """Test to show that get_num_same_species
        return is number of same species(carn)
        """
        i = Island()
        h_1 = Carnivore(i, self.loc)
        h_2 = Carnivore(i, self.loc)

        assert h_1.get_num_same_species(self.loc) == 2

    def test_relative_abundance_gives_output_herb(self):
        """Test to show that relative_abundance returns output for herb
        """
        i = Island()
        jungle_loc = (2,7)
        h = Herbivore(i, jungle_loc)
        self_calculated_abundance = 40
        assert h.relative_abundance(jungle_loc) == self_calculated_abundance

    def test_relative_abundance_gives_output_carn(self):
        """Test to show that relative_abundance returns output for herb
        """
        i = Island()
        jungle_loc = (2,7)
        h = Herbivore(i, jungle_loc, weight = 50)
        c = Carnivore(i, jungle_loc)
        self_calculated_abundance = 0.5
        assert c.relative_abundance(jungle_loc) == self_calculated_abundance

    def test_propensity_0_if_mountain_or_ocean(self):
        """Test to show that propensity returns 0 if cell_type is mountain
        or ocean
        """
        ocean_loc = (0,0)
        mountain_loc = (1,9)
        i = Island()
        h = Herbivore(i, mountain_loc)

        assert h.propensity(ocean_loc) == 0
        assert h.propensity(mountain_loc) == 0

    def test_propensity_return_value_desert(self):
        """Test to show that propensity returns a value based on a formula
         when placed in desert
         """
        i = Island()
        des_loc = (5,9)
        h = Herbivore(i, des_loc)

        assert h.propensity(des_loc) == 1

    def test_get_potential_coordinates_gives_neighbour_coord(self):
        """Test to show that get_potential_coordinates returns the
        neighbouring coordinates
        """
        loc = (2, 2)
        neighbour_coord = [(3, 2), (1, 2), (2, 3), (2, 1)]
        h = Herbivore(self.i, loc)

        assert h.get_potential_coordinates() == neighbour_coord

    def test_total_propensity_surrounded_by_desert(self):
        """Test to show that total_propensity returns value based on
        formula when surrounded by desert
        """
        loc= (6,9)
        h = Herbivore(self.i, loc)
        loc_list = h.get_potential_coordinates()

        assert h.total_propensity(loc_list) == 4

    def test_probabilities_returns_none_surrounded_by_ocean(self):
        """Test to show probabilities returns none when surrounded by ocean
        """
        loc = (1,2)
        h = Herbivore(self.spes_island, loc)
        loc_list = h.get_potential_coordinates()

        assert h.probabilities(loc_list) is None

    def test_probabilities_returns_prob_list(self):
        """Test to show that probabilities returns probability_list based
        on formula
        """
        i = Island()
        loc = (3,7)
        c = Carnivore(i, loc)
        loc_list = c.get_potential_coordinates()
        prob_list = [0.25, 0.25, 0.25, 0.25]

        assert c.probabilities(loc_list) == prob_list

    def test_destination_is_none_surrounded_by_ocean(self):
        """Test to show that destination is none while surrounded
        by ocean
        """
        loc = (1, 2)
        h = Herbivore(self.spes_island, loc)
        loc_list = h.get_potential_coordinates()

        assert h.destination(loc_list) is None

    @patch.object(Herbivore, 'probabilities')
    def test_destination_gives_coordinate(self, mocker):
        """Test to show that destination returns destination when mocked
        to a probability of 100% at different indexes
        """
        mocker.return_value = [1, 0, 0, 0]
        i = Island()
        loc = (2,8)
        h = Herbivore(i, loc)
        loc_list = h.get_potential_coordinates()
        assert h.destination(loc_list) == loc_list[0]
        mocker.return_value = [0, 1, 0, 0]
        assert h.destination(loc_list) == loc_list[1]

    @patch.object(Herbivore, 'will_move')
    def test_migration_removes_pop_from_loc_and_adds_to_odder(self, mocker):
        """Test to show that migration removes population from initial
        loc to the chosen destination when the mocked value for will_move
        is set to True
        """
        mocker.return_value = True
        loc_with_one_place_to_move = (1, 1)
        i = Island(self.spes_geogr_2)
        h = Herbivore(i, loc_with_one_place_to_move)
        old_loc = h.get_loc()
        h.migrate()
        new_loc = h.get_loc()

        assert i.get_num_herb_on_loc(old_loc) == 0
        assert i.get_num_herb_on_loc(new_loc) == 1
        assert old_loc != new_loc

    @patch.object(Herbivore, 'destination')
    @patch.object(Herbivore, 'will_move')
    def test_migration_does_not_happen_if_destination_none(
            self, mocker_1, mocker_2):
        """Test to show that migration does not happen if destination is none.
        destination() is mocked to None, and will_move() is mocked to True.
        """
        mocker_1.return_value = None
        mocker_2.return_value = True
        i = Island()
        loc = (2,7)
        h = Herbivore(i, loc)
        old_loc = h.get_loc()
        h.migrate()
        new_loc = h.get_loc()
        assert old_loc == new_loc #SJEKK GJENNOM HVORFOR DU IKKE FÅR 100%


class TestHerbivore:

    def test_fodder_eaten_for_full_landscapes(self):
        """Test to show that fodder eaten returns the optimal fodder for
        Herbivore when landscape is full, and 0 if landscape is empty
        """
        jungle_loc = (2,7)
        savannah_loc = (2,1)
        ocean_loc = (0,0)
        i = Island()
        j_sim = Herbivore(i, jungle_loc)
        j_sim.fodder_eaten()
        s_sim = Herbivore(i, savannah_loc)
        s_sim.fodder_eaten()
        o_sim = Herbivore(i, ocean_loc)
        o_sim.fodder_eaten()
        optimal_fodder = Herbivore.parameters["F"]

        assert j_sim.fodder_eaten() == optimal_fodder
        assert s_sim.fodder_eaten() == optimal_fodder
        assert o_sim.fodder_eaten() == 0

    def test_fodder_eaten_only_eat_available_fodder(self):
        """Test to show that fodder_eaten only returns the available
        fodder if the location contains less fodder than optimal fodder
        """
        jungle_loc = (2,7)
        Island._param_changer("J", {"f_max" : 5})
        i_sim = Island()
        s_1 = Herbivore(i_sim, jungle_loc)

        assert s_1.fodder_eaten() == 5

    def test_feed_raises_fitness(self):
        """Test to show that feed makes changes to fitness
        """
        loc = (2, 7)
        i = Island()
        h = Herbivore(i, loc)
        old_fitness = h.fitness
        h.feed()
        new_fitness = h.fitness

        assert old_fitness < new_fitness

    def test_eaten_removes_herb(self):
        """Test to show that eaten removes dead herb from location
        """
        i = Island()
        loc = (2, 7)
        a = Herbivore(i, loc)
        ini_pop = a.get_num_same_species(loc)
        a.eaten()
        new_pop = a.get_num_same_species(loc)

        assert ini_pop != new_pop


class TestCarnivore:

    def test_kill_herb_false_if_fitness_too_low(self):
        """Test to show that kill_herb returns False if the Carnivore-fitness
        is too low
        """
        i = Island()
        loc = (2, 7)
        c = Carnivore(i, loc, weight=0)
        h = Herbivore(i, loc, weight=100)

        assert not c.kill_herb(h)

    def test_kill_herb_true_if_prob_1(self, mocker):
        """Test to show that kill_herb returns True if the mocker return
        value is set to lowest
        """
        mocker.patch('random.random', return_value=0)
        i = Island()
        loc = (2, 7)
        c = Carnivore(i, loc, weight=100)
        h = Herbivore(i, loc, weight=0)

        assert c.kill_herb(h)

    def test_kill_herb_true_if_DeltaPhiMax_is_low(self):
        """Test to show that kill_herb returns True if DeltaPhiMax
        is set to 0.
        """
        i = Island()
        loc = (2, 7)
        c = Carnivore(i, loc, weight=100)
        h = Herbivore(i, loc, weight=0)
        c.param_changer({"DeltaPhiMax": 0})

        assert c.kill_herb(h)

    def test_appetite_checker_gives_weight(self):
        """Test to show that appetite_checker returns the weight that the
        Carnivore eats
        """
        i = Island()
        loc = (2, 7)
        c = Carnivore(i, loc)
        e_weight_1 = 30
        d_weight_1 = 50
        last_kill_1 = 100

        e_weight_2 = 30
        d_weight_2 = 50
        last_kill_2 = 20

        e_weight_3 = 30
        d_weight_3 = 50
        last_kill_3 = 5

        assert c.appetite_checker(e_weight_1, d_weight_1, last_kill_1) == 20
        assert c.appetite_checker(e_weight_2, d_weight_2, last_kill_2) == 20
        assert c.appetite_checker(e_weight_3, d_weight_3, last_kill_3) == 5

    @patch.object(Carnivore, 'kill_herb')
    def test_feed_gains_weight(self, mocker):
        """Test to show that feed gains weight when a Herbivore is killed
        by setting the mocked value from kill_herb to True
        """
        mocker.return_value = True
        i = Island()
        loc = (2, 7)
        h = Herbivore(i, loc, weight=40)
        c = Carnivore(i, loc, weight=100)
        old_weight = c.weight
        c.feed()
        new_weight = old_weight + (h.weight * c.parameters["beta"])
        assert c.weight == new_weight
