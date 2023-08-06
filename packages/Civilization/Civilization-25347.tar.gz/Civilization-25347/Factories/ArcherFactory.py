from Units.Archer import Archer
from Factories.Factory import Factory


class ArcherFactory(Factory):

    def create_unit(self, armor_lvl, damage_lvl):
        return Archer(armor_lvl, damage_lvl)
