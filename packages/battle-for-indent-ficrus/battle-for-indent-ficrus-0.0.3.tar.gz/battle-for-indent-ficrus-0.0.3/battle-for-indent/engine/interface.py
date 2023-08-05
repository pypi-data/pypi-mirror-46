from abc import ABC, abstractmethod
import arcade
from options_manager import OptionsManager
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
IMAGE_NAMES = {"Zombie": "../images/zombie/zhead.png", "Knight": "../images/knight/head.png",
               "Paladin": "../images/paladin/head.png", "Walker": "../images/walker/zhead.png"}


class Component(ABC):
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def add(self, component) -> None:
        pass

    def remove(self, component) -> None:
        pass

    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def get_all_elements(self) -> list:
        pass

    @abstractmethod
    def get_leaves(self) -> list:
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self, delta_time: float):
        pass


class Leaf(Component):
    def get_all_elements(self) -> list:
        return []

    def get_leaves(self) -> list:
        return []

    def draw(self):
        pass

    def update(self, delta_time: float):
        pass


class Composite(Component):
    def __init__(self) -> None:
        self._children = []
        self.modified = False
        self.chache = []

    def add(self, component: Component) -> None:
        self._children.append(component)

        component.parent = self

        self.modified = True

    def remove(self, component: Component):
        self._children.remove(component)

        component.parent = None

        self.modified = True

    def is_composite(self) -> bool:
        return True

    def get_all_elements(self) -> list:
        return self._children + sum([child.get_all_elements() for child in self._children], [])

    def get_leaves(self) -> list:
        if self.modified or len(self.chache) == 0:
            self.modified = False
            self.chache = []

            all_elements = self.get_all_elements()

            leaves = [leaf for leaf in all_elements if isinstance(leaf, Leaf)]

            chache = leaves
        
        return chache

    def demonstrate(self) -> None:
        for i in self._children:
            print(i)
            if i.is_composite():
                i.demonstrate()

    def draw(self):
        for child in self._children:
            child.draw()

    def update(self, delta_time: float) -> None:
        for child in self._children:
            child.update(delta_time)


class Text(Leaf):
    def __init__(self, text, center_x, center_y, color=arcade.color.BLACK, font_size=50):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.font_size = font_size
        self.text = text

    def draw(self):
        arcade.draw_text(self.text,
                         self.center_x, self.center_y, self.color, self.font_size)


class Image(Leaf):
    def __init__(self, center_x, center_y, scale, image):
        self.center_x = center_x
        self.center_y = center_y
        self.scale = scale
        self.image = image

    def draw(self):
        sprite = arcade.Sprite(self.image, center_x=self.center_x, center_y=self.center_y, scale=self.scale)
        sprite.draw()


class Stage(Image):
    def __init__(self, image):
        super().__init__(SCREEN_WIDTH / 2, SCREEN_HEIGHT/2, 0.5, image)


class UnitButton(Leaf):
    def __init__(self, unit_job: str) -> None:
        self.unit_job = unit_job

    def draw(self):
        self.portrait = "eeeee"


# Это желательно вынести в другой файл, так как реализует не наполнение state, а наполнение игры
class HealthBar(Leaf):
    def __init__(self, fraction: str) -> None:
        self.fraction = fraction

    def draw(self):
        self.hp = 100


class PauseButton(Leaf):
    def __init__(self) -> None:
        pass

    def draw(self):
        pass


# Это желательно вынести в другой файл, так как реализует не наполнение state, а наполнение игры
class Castle(Leaf):
    def __init__(self, fraction):
        self.fraction = fraction

    def draw(self):
        pass


class Button(Leaf):
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


class CooldownIndicator(Leaf):
    def __init__(self,
                 center_x, center_y,
                 width, height,
                 unit_type,
                 unit_num,
                 cool_down,
                 key,
                 font_size=16,
                 font_face="Arial",
                 ready_color=arcade.color.BABY_BLUE,
                 unready_color=arcade.color.PASTEL_GRAY,
                 line_color=arcade.color.GRAY,
                 line_height=2,
                 circle_color=arcade.color.WHITE):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_face = font_face
        self.ready_color = ready_color
        self.unready_color = unready_color
        self.line_height = line_height
        self.TIME = 0
        self.cool_down = cool_down
        self.unit_type = unit_type
        self.unit_num = unit_num
        self.is_ready = True
        self.line_color = line_color
        self.circle_color = circle_color
        self.key = key

    def update(self, delta_time: float):
        if self.is_ready is False:
            self.TIME += delta_time
            if self.TIME > self.cool_down:
                self.is_ready = True
                self.TIME = 0

    def draw(self):
        if not self.is_ready:
            color = self.unready_color
        else:
            color = self.ready_color
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, color)

        if not self.is_ready:
            height = self.TIME * self.height / self.cool_down
            arcade.draw_rectangle_filled(self.center_x, self.center_y - self.height / 2 + height / 2, self.width,
                                         height,
                                         self.ready_color)

        color = self.line_color

        sprite = arcade.Sprite(IMAGE_NAMES[self.unit_type], center_x=self.center_x, center_y=self.center_y, scale=0.25)
        sprite.draw()

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.line_height)

        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.line_height)

        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.line_height)

        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.line_height)

        x = self.center_x + 0.65 * self.width / 2
        y = self.center_y - self.height / 2 + 0.7 * self.width / 4
        arcade.draw_circle_filled(x, y, self.width / 4, self.circle_color)
        arcade.draw_text(str(self.unit_num), x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_choose(self):
        if self.unit_num > 0 and self.is_ready is True:
            self.unit_num -= 1
            self.is_ready = False
            return True
        else:
            return False


class RoadSelection(Leaf):
    def __init__(self):
        self.selected_road = 0

    def draw(self):
        if self.selected_road > 0:
            y = SCREEN_HEIGHT*(3 - self.selected_road)/3 + SCREEN_HEIGHT/10
            sprite = arcade.Sprite("../images/stage/road.png", center_x=SCREEN_WIDTH/2, center_y=y, scale=0.5)
            sprite.draw()


class MenuButton(Button):
    def __init__(self, center_x, center_y, width, height, text, action_function, argument=None):
        self.action_function = action_function
        self.argument = argument
        super().__init__(center_x, center_y, width, height, text)

    def on_release(self):
        super().on_release()

        if OptionsManager().is_sounds_enabled:
            click_sound = arcade.load_sound("../sounds/click-sound.wav")
            arcade.play_sound(click_sound)

        if self.argument is None:
            self.action_function()
        else:
            self.action_function(self.argument)
