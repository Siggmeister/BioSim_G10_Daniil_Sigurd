# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov', 'Sigurd Grøtan'
__email__ = 'daniil.vitalevich.efremov@nmbu.no', 'sgrotan@nmbu.no'

from src.biosim.simulation import BioSim
_FFMPEG_BINARY = r"ffmpeg"


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
                {"species": "Herbivore", "age": 5, "weight": 200}
                for _ in range(150)
            ],
        }

    ]

    carn_pop = [{
            "loc": (2, 7),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(20)
            ],
        }]

    s = BioSim(geogr, ini_herbs, img_base=r"C:\Users\Sigur\OneDrive\Dokumenter\INF200\Phoetoes\BioSim")
    s.set_landscape_parameters("J", {"f_max": 700})

    s.simulate(10)
    s.add_population(carn_pop)
    s.simulate(100)
    s.make_movie()
    print("======================")