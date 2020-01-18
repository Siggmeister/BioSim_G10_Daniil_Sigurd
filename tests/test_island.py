# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov'
__email__ = 'daniil.vitalevich.efremov@nmbu.no'

from src.biosim.island import *
from src.biosim.landscape import *
import pytest


class TestIsland:

    def test_island_instance(self):
        i = Island()
        assert isinstance(i, Island)

    def test_check_geo_string(self):
        geo_string_1 = """\
                    OOOOOOOOOOOO
                    OOOJJSSSSMMM
                    OSSSSSJJJJMM
                    """
        with pytest.raises(ValueError):
            Island._check_geo_string(geo_string_1)

        geo_string_2 = """\
                    OOOOOOOOOOOO
                    OOOJJSSSSMMOOO
                    OOOOOOOOOOOOOOOO
                    """
        with pytest.raises(ValueError):
            Island._check_geo_string(geo_string_2)

    def test_geo_string_works_with_upper_and_lower_case(self):
        geo_string = """\
                    OOOOOOOOoOOO
                    OOOJJSSSsMMO
                    OSSSsSJjJJMO
                    OOOoOOOOoooO
                    """
        island_dict = Island._island_dict_maker(geo_string)
        for loc in island_dict:
            assert isinstance(island_dict[loc], Landscape)