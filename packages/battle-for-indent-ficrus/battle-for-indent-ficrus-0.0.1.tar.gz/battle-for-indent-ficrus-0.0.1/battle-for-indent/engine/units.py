from abc import ABC, abstractmethod
from interface import Leaf
import arcade


class BaseUnit(Leaf):
    def __init__(self, sprite=None, x=0, y=0, scale=1, mirrored=False):
        self.sprite = None
        if sprite is not None:
            self.sprite = sprite(scale=scale, mirrored=mirrored)
        self.fraction = ""
        self.job = ""
        self.description = ""
        self.power = 0
        self.hp = 0
        self.max_hp = 0
        self.physical_damage = 0
        self.magical_damage = 0
        self.physical_resist = 0
        self.magical_resist = 0
        self.move_speed = 0
        self.setup(x, y)

    @abstractmethod
    def accept(self, visitor) -> None:
        pass

    def setup(self, x, y):
        if self.sprite is not None:
            self.sprite.setup(x, y)
            self.sprite.move_speed = self.move_speed

    def draw(self):
            if self.sprite is not None:
                self.sprite.on_draw()
            if self.hp > self.max_hp * 0.5:
                arcade.draw_rectangle_filled(self.sprite.center_x,
                                             self.sprite.center_y + 100,
                                             width=self.hp / self.max_hp * 50, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_GREEN)
            elif self.hp > self.max_hp * 0.25:
                arcade.draw_rectangle_filled(self.sprite.center_x,
                                             self.sprite.center_y + 100,
                                             width=self.hp / self.max_hp * 50, height=self.max_hp / 50,
                                             color=arcade.color.LIGHT_YELLOW)
            elif self.hp > 0:
                arcade.draw_rectangle_filled(self.sprite.center_x,
                                             self.sprite.center_y + 100,
                                             width=self.hp / self.max_hp * 50, height=self.max_hp / 50,
                                             color=arcade.color.DARK_RED)

            arcade.draw_rectangle_outline(self.sprite.center_x,
                                          self.sprite.center_y + 100,
                                          width=52, height=self.max_hp / 50 + 2, color=arcade.color.DARK_GREEN)

    def update(self, delta_time):
        if self.sprite is not None:
            self.sprite.update(delta_time)

    def attack(self, target, target_army=None, damage=0):
        if damage == 0:
            damage = self.physical_damage
        target.hp -= damage
        if target.hp <= 0:
            if target in target_army.units.get_leaves():
                target_army.units.remove(target)


class Knight(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=0.16, mirrored=False):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale, mirrored=mirrored)

        self.job = "Knight"
        self.description = "Strong and self-confident knight"
        self.power = 10
        self.hp = 500
        self.max_hp = self.hp
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 0.5
        self.magical_resist = 0
        self.move_speed = 0.8
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target, target_army=None, damage=0):
        super().attack(target, target_army)

    def accept(self, visitor) -> None:
        visitor.visit_knight(self)


class Paladin(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=1, mirrored=False):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale, mirrored=mirrored)

        self.job = "Paladin"
        self.description = "Master of spear and base magic"
        self.power = 20
        self.hp = 1000
        self.max_hp = self.hp
        self.physical_damage = 5
        self.magical_damage = 0
        self.physical_resist = 0.2
        self.magical_resist = 0
        self.move_speed = 1
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target, target_army=None, damage=0):
        super().attack(target, target_army)

    def accept(self, visitor) -> None:
        visitor.visit_paladin(self)


class Zombie(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=0.15, mirrored=False):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale, mirrored=mirrored)

        self.job = "Zombie"
        self.description = "It's not a bandit at all"
        self.power = 10
        self.hp = 300
        self.max_hp = self.hp
        self.physical_damage = 6
        self.magical_damage = 0
        self.physical_resist = 0.2
        self.magical_resist = 0
        self.move_speed = 0.5
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target, target_army=None, damage=0):
        super().attack(target, target_army)

    def accept(self, visitor) -> None:
        visitor.visit_zombie(self)


class Walker(BaseUnit):
    def __init__(self, sprite=None, x=0, y=0, scale=0.15):
        super().__init__(sprite=sprite, x=x, y=y, scale=scale)

        self.job = "Walker"
        self.description = "Freezing death incarnate"
        self.power = 20
        self.hp = 6000
        self.max_hp = self.hp
        self.physical_damage = 2
        self.magical_damage = 0
        self.physical_resist = 0.5
        self.magical_resist = 0
        self.move_speed = 0.3
        if self.sprite is not None:
            self.sprite.move_speed = self.move_speed

    def attack(self, target, target_army=None, damage=0):
        super().attack(target, target_army)

    def accept(self, visitor) -> None:
        visitor.visit_walker(self)


def get_decription(UnitClass: BaseUnit) -> str:
    full_dectiption = """
    This is {u.job}
    {u.description}
    Stats:
        Power Cost: {u.power}
        HP: {u.hp}
        Physical Damage: {u.physical_damage}
        Magical Damage: {u.magical_damage}
        Physical Resist: {u.physical_resist}
        Magical Resist: {u.magical_resist}
        Move Speed: {u.move_speed}
    """.format(u=UnitClass())

    return full_dectiption


class Visitor(ABC):
    @abstractmethod
    def visit_knight(self, element) -> None:
        pass

    @abstractmethod
    def visit_paladin(self, element) -> None:
        pass

    @abstractmethod
    def visit_zombie(self, element) -> None:
        pass

    @abstractmethod
    def visit_walker(self, element) -> None:
        pass


class LeftArmyVisitor(Visitor):
    def __init__(self, armies):
        self.armies = armies
        self.other_army_sprite_list = list()
        for unit in armies[1].units.get_leaves():
            spritelist = arcade.SpriteList()
            for part in unit.sprite.object_parts:
                spritelist.append(part.sprite)
            self.other_army_sprite_list.append([unit, spritelist])

    def visit_knight(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[1], damage=element.physical_damage*enemy[0].physical_resist)
        if flag != 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_right = True

    def visit_paladin(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[1])
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_right = True

    def visit_zombie(self, element) -> None:
        """Тут, вообще говоря, может быть другая логика атаки и движения"""
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[1], damage=element.physical_damage*enemy[0].physical_resist)
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_right = True

    def visit_walker(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[1])
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_right = True


class RightArmyVisitor(Visitor):
    def __init__(self, armies):
        self.armies = armies
        self.other_army_sprite_list = list()
        for unit in armies[0].units.get_leaves():
            spritelist = arcade.SpriteList()
            for part in unit.sprite.object_parts:
                spritelist.append(part.sprite)
            self.other_army_sprite_list.append([unit, spritelist])

    def visit_knight(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[0], damage=element.physical_damage*enemy[0].physical_resist)
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_left = True

    def visit_paladin(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[0])
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_left = True

    def visit_zombie(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[0], damage=element.physical_damage*enemy[0].physical_resist)
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_left = True

    def visit_walker(self, element) -> None:
        flag = 0
        for part in element.sprite.object_parts:
            for enemy in self.other_army_sprite_list:
                k = len(arcade.check_for_collision_with_list(part.sprite, enemy[1]))
                if k > 0:
                    flag = 1
                    element.attack(enemy[0], self.armies[0])
        if flag > 0:
            element.sprite.move_left = False
            element.sprite.move_right = False
            if not element.sprite.start_attack:
                element.sprite.attack = True
        else:
            element.sprite.start_attack = False
            element.sprite.attack = False
            element.sprite.move_left = True

