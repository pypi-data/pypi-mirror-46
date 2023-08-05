from units import *
from sprite import KnightSprite, ZombieSprite, WalkerSprite, PaladinSprite


class Singleton(ABC, type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UnitFactory(metaclass=Singleton):
    @abstractmethod
    def create(self, x=0, y=0):
        pass


class KnightFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0, mirrored=False) -> BaseUnit:
        knight = Knight(sprite=KnightSprite, x=x, y=y, scale=scale, mirrored=mirrored)
        if road == 1:
            knight.sprite.set_speed_decorator(1.5)
            knight.sprite.move_speed *= 1.5
        if road == 3:
            knight.sprite.set_speed_decorator(0.6)
            knight.sprite.move_speed *= 0.8
        return knight


class ZombieFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0, mirrored=False) -> BaseUnit:
        zombie = Zombie(sprite=ZombieSprite, x=x, y=y, scale=scale, mirrored=mirrored)
        if road == 1:
            zombie.sprite.set_speed_decorator(1.4)
        if road == 3:
            zombie.sprite.set_speed_decorator(0.7)
        return zombie


class PaladinFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0, mirrored=False) -> BaseUnit:
        paladin = Paladin(sprite=PaladinSprite, x=x, y=y, scale=scale, mirrored=mirrored)
        if road == 1:
            paladin.sprite.set_speed_decorator(1.4)
        if road == 3:
            paladin.sprite.set_speed_decorator(0.7)
        return paladin


class WalkerFactory(UnitFactory):
    def create(self, x=0, y=0, scale=0.20, road=0, mirrored=False) -> BaseUnit:
        walker = Paladin(sprite=WalkerSprite, x=x, y=y, scale=scale, mirrored=mirrored)
        if road == 1:
            walker.sprite.set_speed_decorator(1.4)
        if road == 3:
            walker.sprite.set_speed_decorator(0.7)
        return walker