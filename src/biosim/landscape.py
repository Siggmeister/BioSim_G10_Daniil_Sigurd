
class Landscape:
    landscape_parameters = {"J": {"f_max": 800.0},
                            "S": {"f_max": 300.0,
                                  "alpha": 0.3}}

    def __init__(self):
        self.herb_pop = 0
        self.carn_pop = 0
        self.available = None
        self.fodder = None

    def add_pop(self, animal):
        if animal.__class__.__name__ == "Herbivore":
            self.herb_pop += 1
        elif animal.__class__.__name__ == "Carnivore":
            self.carn_pop += 1

    def remove_pop(self, animal):
        if animal.__class__.__name__ == "Herbivore":
            self.herb_pop -= 1
        elif animal.__class__.__name__ == "Carnivore":
            self.carn_pop -= 1

    def fodder_annual_refill(self):
        pass

    def get_fodder(self):
        return self.fodder

    def get_availability(self):
        return self.available

    def herb_eats_fodder(self, fodder_eaten):
        if self.fodder is not None:
            self.fodder -= fodder_eaten

    @classmethod
    def param_changer(cls, landscape, new_param):
        for key in new_param:
            Landscape.landscape_parameters[landscape][key] = new_param[key]


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
