# -*- coding: utf-8 -*-

__author__ = 'Daniil Efremov', 'Sigurd Grøtan'
__email__ = 'daniil.vitalevich.efremov@nmbu.no', 'sgrotan@nmbu.no'


class Landscape:
    """This is the base class for all the different types
     of landscape classes occurring in the island geography.
    """
    landscape_parameters = {"J": {"f_max": 800.0},
                            "S": {"f_max": 300.0,
                                  "alpha": 0.3}}

    def __init__(self):
        """Constructor method.
        """
        self.herb_pop_list = []
        self.carn_pop_list = []
        self.fodder = 0

    def add_pop(self, animal):
        """Adds an animal instance to the appropriate animal list on cell

        :param animal: An instance of either
        <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        with data and methods, containing info about the animal.
        :type animal: <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        """
        if animal.__class__.__name__ == "Herbivore":
            self.herb_pop_list.append(animal)
        elif animal.__class__.__name__ == "Carnivore":
            self.carn_pop_list.append(animal)

    def remove_pop(self, animal):
        """Removes an animal instance of the appropriate animal list on cell

        :param animal: An instance of either
        <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        with data and methods, containing info about the animal.
        :type animal: <class 'src.biosim.animals.Herbivore'> or
        <class 'src.biosim.animals.Carnivore'>
        """
        if animal.__class__.__name__ == "Herbivore":
            self.herb_pop_list.remove(animal)
        elif animal.__class__.__name__ == "Carnivore":
            self.carn_pop_list.remove(animal)

    def fodder_annual_refill(self):
        """Empty fodder_refill method being passed to all subclasses of
        Landscape.
        """
        pass

    def get_fodder(self):
        """Returns fodder on cell.

        :return: Fodder
        :rtype: float
        """
        return self.fodder

    def herb_eats_fodder(self, fodder_eaten):
        """Subtracts amount of fodder_eaten by Herbivore from initial fodder
        on cell.

        :param fodder_eaten: Amount of fodder eaten by Herbivore
        :type fodder_eaten: float
        """
        self.fodder -= fodder_eaten

    def get_herb_pop_list(self):
        """Returns population list for Herbivores on cell.

        :return: Herbivore population list
        :rtype: list
        """
        return self.herb_pop_list

    def get_carn_pop_list(self):
        """Returns population list for Carnivores on cell.

        :return: Carnivore population list
        :rtype: list
        """
        return self.carn_pop_list

    def get_num_herb(self):
        """Returns number of Herbivores on cell.

        :return: Number of Herbivores
        :rtype: int
        """
        return len(self.herb_pop_list)

    def get_num_carn(self):
        """Returns number of Carnivores on cell.

        :return: Number of Carnivores
        :rtype: int
        """
        return len(self.carn_pop_list)

    def sort_pop_by_fitness(self):
        """Sorts all animals by fitness. Updates the carnivore and herbivore
        pop list to be sorted.
        """
        self.herb_pop_list.sort(key=lambda herb: herb.fitness, reverse=True)
        self.carn_pop_list.sort(key=lambda carn: carn.fitness, reverse=True)

    def get_total_herb_weight(self):
        """Returns the total weight of Herbivores on cell.

        :return: Total weight of Herbivores
        :rtype: float
        """
        total_weight = 0
        for herb in self.get_herb_pop_list():
            total_weight += herb.weight
        return total_weight

    @classmethod
    def param_changer(cls, landscape, new_params):
        """Changes parameters for the cells in landscape.

        :param landscape: One letter string containing the landscape_code
        for either Jungle or Savannah.
        :type landscape: str
        :param new_params: dictionary containing the parameters to change
        :type new_params: dict
        """
        Landscape.landscape_parameters[landscape].update(new_params)


class Jungle(Landscape):
    """SUMMARY
    """

    def __init__(self):
        """SUMMARY
        """
        super().__init__()
        self.fodder = Landscape.landscape_parameters["J"]["f_max"]

    def fodder_annual_refill(self):
        """Overrides the initial fodder_refill method from Landscape
        parent-class, and sets the fodder to max-value for jungle"""
        self.fodder = Landscape.landscape_parameters["J"]["f_max"]


class Savannah(Landscape):
    """SUMMARY
    """

    def __init__(self):
        """SUMMARY
        """
        super().__init__()
        self.fodder = Landscape.landscape_parameters["S"]["f_max"]

    def fodder_annual_refill(self):
        """Overrides the initial fodder_refill method from Landscape
        parent-class, and changes the fodder according to formula.
        """
        f_max_savannah = Landscape.landscape_parameters["S"]["f_max"]
        alpha = Landscape.landscape_parameters["S"]["alpha"]
        self.fodder += (alpha * (f_max_savannah-self.fodder))
        if self.fodder > f_max_savannah:
            self.fodder = f_max_savannah


class Desert(Landscape):
    """SUMMARY
    """

    def __init__(self):
        """SUMMARY
        """
        super().__init__()


class Mountain(Landscape):
    """SUMMARY
    """

    def __init__(self):
        """SUMMARY
        """
        super().__init__()


class Ocean(Landscape):
    """SUMMARY
    """

    def __init__(self):
        """SUMMARY
        """
        super().__init__()
