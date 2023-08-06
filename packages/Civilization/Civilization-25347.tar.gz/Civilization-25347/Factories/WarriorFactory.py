from Units.Warrior import Warrior
from Factories.Factory import Factory


class WarriorFactory(Factory):

    def create_unit(self, armor_lvl, damage_lvl):
        return Warrior(armor_lvl, damage_lvl)
