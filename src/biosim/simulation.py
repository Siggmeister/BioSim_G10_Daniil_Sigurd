# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

from island import *
from animals import *
from annual_cycle import *
import matplotlib.pyplot as plt
import textwrap
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
import numpy as np
import random as rd
from matplotlib.widgets import Button
import subprocess



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
        rd.seed(seed)
        np.random.seed(seed)

        island_map = textwrap.dedent(island_map)
        self._island_map = island_map
        self.island = Island(self._island_map)
        self.cycle = AnnualCycle(self.island)
        self.add_population(ini_pop)

        self._n_rows = len(island_map.splitlines())
        self._n_columns = len(island_map.splitlines()[0]) # LAG METHOD

        self._img_base = img_base
        self._img_fmt = img_fmt

        self._herbivore_line = None
        self._carnivore_line = None

        self._herbs = []
        self._carns = []
        self._animals = []
        self._vis_years = []

        self._slwidth = 0.08  # Width of sliders and buttons
        self._spos1 = 0.6  # x-placement of sliders col 1
        self._spos2 = 0.8


        self._year = 0
        self._final_year = None
        self._img_ctr = 0

        self._num_animals = None
        self._num_animal_per_species = None
        self._animal_distribution = None
        self._max_animals = None

        self._fig = None
        self._map_ax = None
        self._animal_ax = None
        self._herb_dist_ax = None
        self._carn_dist_ax = None
        self._herb_dist_plot = None
        self._carn_dist_plot = None

        self._ax_pause = None
        self._w_pause = None
        self._ax_interrupt = None
        self._w_interrupt = None

        self._paused = False
        self._interrupt = False

        if ymax_animals is not None:
            self._ymax_animals = ymax_animals
        else:
            self._ymax_animals = None

        if cmax_animals is not None:
            self._cmax_herbivore = cmax_animals['Herbivore']
            self._cmax_carnivore = cmax_animals['Carnivore']
        else:
            self._cmax_herbivore = 300
            self._cmax_carnivore = 100


    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == "Herbivore":
            Herbivore.param_changer(params)
        elif species == "Carnivore":
            Carnivore.param_changer(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        self.island._param_changer(landscape, params)

    def island_map(self):
        self._map_ax = self._fig.add_axes([0.05, 0.7, 0.25, 0.25])
        color_code = {
            "O": mcolors.to_rgba("navy"),
            "J": mcolors.to_rgba("forestgreen"),
            "S": mcolors.to_rgba("#e1ab62"),
            "D": mcolors.to_rgba("salmon"),
            "M": mcolors.to_rgba("lightslategrey"),
        }

        kart_rgb = [[color_code[column] for column in row]
                    for row in self._island_map.splitlines()]

        self._map_ax.imshow(kart_rgb)
        self._map_ax.set_title('Island map', fontsize=18)

    def _setup_graphics(self):

        if self._fig is None:
            self._fig = plt.figure(figsize=(18, 12))

        if self._map_ax is None:
            self.island_map()

        if self._animal_ax is None:
            self._animal_ax = self._fig.add_axes([0.4, 0.4, 0.5, 0.5])

            if self._ymax_animals is not None:
                self._animal_ax.set_ylim(0, self._ymax_animals)

            else:
                self._max_animals = self.num_animals
                self._animal_ax.set_ylim(0, self._max_animals * 1.1) #OBS
            self._animal_ax.set_title("Population\n\n ")
            self._animal_ax.set_xlabel("# Years")
            self._animal_ax.set_ylabel("# animals")

        self._animal_ax.set_xlim(0, self._final_year + 1)

        if self._herbivore_line is None:
            herbivore_plot = self._animal_ax.plot(np.arange(0, self._final_year),
                                                  np.full(self._final_year, np.nan),
                                                  label='Herbivores')
            self._herbivore_line = herbivore_plot[0]
        else:
            xdata, ydata = self._herbivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._herbivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

        if self._carnivore_line is None:
            carnivore_plot = self._animal_ax.plot(np.arange(0, self._final_year),
                                                  np.full(self._final_year, np.nan),
                                                  label='Carnivores')
            self._carnivore_line = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._carnivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

        if self._herb_dist_ax is None:
            self._herb_dist_ax = self._fig.add_axes([0.05, 0.4, 0.25, 0.25])
            self._herb_dist_ax.set_title("Herbivore distribution")

        if self._herb_dist_plot is None:
            self._herb_dist_plot = self._herb_dist_ax.imshow(np.reshape(self.animal_distribution[
                                                                            'Herbivore'].values,
                                                                        newshape=(self._n_rows,
                                                                                  self._n_columns)),
                                                             interpolation='none',
                                                             vmin=0.9, vmax=self._cmax_herbivore)
            plt.colorbar(mappable=self._herb_dist_plot)
        else:
            self._herb_dist_plot.set_data(np.reshape(self.animal_distribution['Herbivore'].values,
                                                     newshape=(self._n_rows, self._n_columns)))

        if self._carn_dist_ax is None:
            self._carn_dist_ax = self._fig.add_axes([0.05, 0.1, 0.25, 0.25])
            self._carn_dist_ax.set_title("Carnivore distribution")

        if self._carn_dist_plot is None:
            self._carn_dist_plot = self._carn_dist_ax.imshow(np.reshape(self.animal_distribution[
                                                                            'Carnivore'].values,
                                                                        newshape=(self._n_rows,
                                                                                  self._n_columns)),
                                                             interpolation='none',
                                                             vmin=0.9, vmax=self._cmax_carnivore)
            plt.colorbar(mappable=self._carn_dist_plot)
        else:
            self._carn_dist_plot.set_data(np.reshape(self.animal_distribution[
                                                         'Carnivore'].values,
                                                     newshape=(self._n_rows, self._n_columns)))

        # Button to pause/run
        if self._ax_pause is None:
            self._ax_pause = self._fig.add_axes([self._spos1, 0.10, self._slwidth, 0.03])
            self._w_pause = Button(self._ax_pause, 'Pause/Run', hovercolor='0.975')
            self._w_pause.on_clicked(self._change_pause_status)

            # Button to interrupt
        if self._ax_interrupt is None:
            self._ax_interrupt = self._fig.add_axes([self._spos1, 0.05, self._slwidth, 0.03])
            self._w_interrupt = Button(self._ax_interrupt,
                                       'Interrupt',
                                       hovercolor='0.975')
            self._w_interrupt.on_clicked(self._stop_sim)

    def _update_animal_ax(self):
        ydata = self._herbivore_line.get_ydata()
        ydata[self.year] = self.num_animals_per_species['Herbivore']
        self._herbivore_line.set_ydata(ydata)

        ydata = self._carnivore_line.get_ydata()
        ydata[self.year] = self.num_animals_per_species['Carnivore']
        self._carnivore_line.set_ydata(ydata)
        self._animal_ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                               ncol=2, mode="expand", borderaxespad=0.)

    def _update_heatmap_axes(self):
        self._herb_dist_plot.set_data(np.reshape(a=self.animal_distribution['Herbivore'].values,
                                                 newshape=(self._n_rows, self._n_columns)))
        self._carn_dist_plot.set_data(np.reshape(a=self.animal_distribution['Carnivore'].values,
                                                 newshape=(self._n_rows, self._n_columns)))

    def _update_graphics(self):
        """Updates graphics with current data."""
        self._update_animal_ax()
        self._update_heatmap_axes()
        #self._update_text()
        # ylimit for the animal ax:
        if self._ymax_animals is None:
            if self.num_animals > self._max_animals:
                self._max_animals = self.num_animals
                self._animal_ax.set_ylim(0, self._max_animals + 100)
        plt.pause(1e-2)


    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()

        while self.year < self._final_year:
            if self.year % vis_years == 0:
                self._update_graphics()

            if self.year % img_years == 0:
                #self._save_graphics()
                pass

            self.cycle.run_cycle()
            self._year += 1

            if self._interrupt:
                break
            while self._paused:
                plt.pause(0.05)

        self._interrupt = False


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

        for loc_dict in population:

            element_list = ["loc", "pop"]
            for element in element_list:
                if element not in loc_dict:
                    raise ValueError("The population-input should have"
                                     " the elements 'loc' and 'pop'")

            loc = loc_dict["loc"]

            if loc not in self.island.island_dict:
                raise ValueError("The location {0} does not exist "
                                 "in the given Island".format(loc))

            cell_type = self.island.get_cell_type(loc)
            if cell_type == "Ocean" or cell_type == "Mountain":
                raise ValueError("Animal can not be placed "
                                 "in mountain or ocean!")

            for animal_dict in loc_dict["pop"]:
                element_list = ["species", "age", "weight"]
                for element in element_list:
                    if element not in animal_dict:
                        raise ValueError("pop should have the elements"
                                         " 'species', 'age' and 'weight'")

                age = animal_dict["age"]
                weight = animal_dict["weight"]
                if age < 0 or not isinstance(age, int):
                    raise ValueError("The age needs to be a positive integer")
                if weight < 0 or not isinstance(weight, (int, float)):
                    raise ValueError("The weight needs to be a positive number")

                if animal_dict["species"] == "Herbivore":
                    Herbivore(self.island, loc, age, weight)
                elif animal_dict["species"] == "Carnivore":
                    Carnivore(self.island, loc, age, weight)
                else:
                    raise ValueError("The species must be of either"
                                     " Herbivore or Carnivore")



    @property
    def year(self):
        """Last year simulated."""
        return self._year


    @property
    def num_animals(self):
        """Total number of animals on island."""
        self._num_animals = len(self.island.get_all_herb_list()) + \
                            len(self.island.get_all_carn_list())
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        self._num_animal_per_species = {
            "Herbivore": len(self.island.get_all_herb_list()),
            "Carnivore": len(self.island.get_all_carn_list())
        }
        return self._num_animal_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""
        df = pd.DataFrame(self.island.island_data, columns=["row", "col", "Herbivore", "Carnivore"])
        return df

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

    def _stop_sim(self, event):
        """
        Change self._paused flag when pause button is clicked
        """
        print('\nInterrupt button clicked')
        print('    {}'.format(event))
        self._interrupt = True

    def _change_pause_status(self, event):
        """
        Change self._paused flag when pause button is clicked
        """
        print('\nPause button clicked')
        print('    {}'.format(event))
        if self._paused:
            self._paused = False
        else:
            self._paused = True



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
                {"species": "Herbivore", "age": 45, "weight": 200}
                for _ in range(150)
            ],
        },

    ]

    carn_pop = [{
            "loc": (2, 7),
            "pop": [
                {"species": "Carnivore", "age": 55, "weight": 20}
                for _ in range(20)
            ],
        }]

    s = BioSim(geogr, ini_herbs)
    #s.set_landscape_parameters("J", {"f_max": 700})

    #s.simulate(100, vis_years=1)
    #s.add_population(carn_pop)
    #s.simulate(300 ,vis_years=1)



