# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from src.biosim.simulation import BioSim

if __name__ == "__main__":
    i_map = """\
    OOOOOOOOOO
    ODDDDDDDDO
    ODDDDDDDDO
    ODDDDDDDDO
    ODDDDDDDDO
    ODDDDDDDDO
    ODDDDDDDDO
    ODDDDDDDDO
    ODDDDDDDDO
    OOOOOOOOOO"""

    ini_pop = [
        {
            "loc": (5, 5),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(500)
            ],
        },
        {
        "loc": (5, 5),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(500)
        ],
    }
]

    cmax = {"Herbivore": 200, "Carnivore": 50}
    sim = BioSim(i_map, ini_pop, cmax_animals=cmax)

    sim.set_animal_parameters('Herbivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'a_half': 1000})
    sim.set_animal_parameters('Carnivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'a_half': 1000})

    sim.simulate(100)