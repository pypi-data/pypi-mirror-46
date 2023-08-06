from Units.Cavalry import Cavalry
from Factories.Factory import Factory


class CavalryFactory(Factory):

    def create_unit(self, armor_lvl, damage_lvl):
        return Cavalry(armor_lvl, damage_lvl)
