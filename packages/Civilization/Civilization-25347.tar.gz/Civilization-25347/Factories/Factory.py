from abc import ABC, abstractmethod


class Factory(ABC):
    @abstractmethod
    def create_unit(self, armor_lvl, damage_lvl):
        raise NotImplementedError
