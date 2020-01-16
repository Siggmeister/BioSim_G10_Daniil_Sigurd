
class Landscape:
    landscape_parameters = {"J": {"f_max": 800.0},
                            "S": {"f_max": 300.0,
                                  "alpha": 0.3}}

    def __init__(self):
        self.herb_pop_list = []
        self.carn_pop_list = []
        self.available = None
        self.fodder = 0

    def add_pop(self, animal):
        if animal.__class__.__name__ == "Herbivore":
            self.herb_pop_list.append(animal)
        elif animal.__class__.__name__ == "Carnivore":
            self.carn_pop_list.append(animal)

    def remove_pop(self, animal):
        if animal.__class__.__name__ == "Herbivore":
            self.herb_pop_list.remove(animal)
        elif animal.__class__.__name__ == "Carnivore":
            self.carn_pop_list.remove(animal)

    def fodder_annual_refill(self):
        pass

    def get_fodder(self):
        return self.fodder

    def get_availability(self):
        return self.available

    def herb_eats_fodder(self, fodder_eaten):
        self.fodder -= fodder_eaten

    def get_herb_pop_list(self):
        return self.herb_pop_list

    def get_carn_pop_list(self):
        return self.carn_pop_list

    def get_num_herb(self):
        return len(self.herb_pop_list)

    def get_num_carn(self):
        return len(self.carn_pop_list)

    def sort_pop_by_fitness(self):
        self.herb_pop_list.sort(key=lambda herb: herb.fitness, reverse=True)
        self.carn_pop_list.sort(key=lambda carn: carn.fitness, reverse=True)

    def get_total_herb_weight(self):
        total_weight = 0
        for herb in self.get_herb_pop_list():
            total_weight += herb.weight
        return total_weight

    @classmethod
    def param_changer(cls, landscape, new_param):

        Landscape.landscape_parameters[landscape].update(new_param)


class Jungle(Landscape):

    def __init__(self):
        super().__init__()
        self.available = True
        self.fodder = Landscape.landscape_parameters["J"]["f_max"]

    def fodder_annual_refill(self):
        self.fodder = Landscape.landscape_parameters["J"]["f_max"]


class Savannah(Landscape):

    def __init__(self):
        super().__init__()
        self.available = True
        self.fodder = Landscape.landscape_parameters["S"]["f_max"]

    def fodder_annual_refill(self):
        f_max_savannah = Landscape.landscape_parameters["S"]["f_max"]
        alpha = Landscape.landscape_parameters["S"]["alpha"]
        self.fodder += (alpha * (f_max_savannah-self.fodder))
        if self.fodder > f_max_savannah:
            self.fodder = f_max_savannah


class Desert(Landscape):

    def __init__(self):
        super().__init__()
        self.available = True


class Mountain(Landscape):

    def __init__(self):
        super().__init__()
        self.available = False


class Ocean(Landscape):

    def __init__(self):
        super().__init__()
        self.available = False
