# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from island import *
from animals import *
from annual_cycle import *


class TestAnnualCycle:

    def test_weight_loss(self):
        i = Island()
        carn = Carnivore(i, (2, 7), age=5, weight=20)
        herb = Herbivore(i, (2, 7), age=5, weight=20)
        ini_carn_weight = carn.weight
        ini_herb_weight = herb.weight
        cycle = AnnualCycle(i)
        cycle.weight_loss()

        assert carn.weight < ini_carn_weight
        assert herb.weight < ini_herb_weight

    def test_animal_death(self):
        pass



