import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import textwrap
from simulation import *
class Visualiser:

    kart = """\
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

    kart = textwrap.dedent(kart)
    def __init__(self):
        fig = plt.figure()
        self.ax1 = fig.add_subplot(221)
        self.ax2 = fig.add_subplot(222)
        self.ax3 = fig.add_subplot(223)
        self.ax4 = fig.add_subplot(224)

    def island_map(self):
        color_code = {
            "O": mcolors.to_rgba("navy"),
            "J": mcolors.to_rgba("forestgreen"),
            "S": mcolors.to_rgba("#e1ab62"),
            "D": mcolors.to_rgba("salmon"),
            "M": mcolors.to_rgba("lightslategrey"),
        }

        kart_rgb = [[color_code[column] for column in row]
                    for row in self.kart.splitlines()]

        self.ax1.imshow(kart_rgb)
        self.ax1.set_title('Island map', fontsize=10)

    def population_plot(self):

        self.ax2.set_title('Population change', fontsize=10)

    def plot_show(self):
        plt.show()


g = Visualiser()
g.island_map()
g.plot_show()




