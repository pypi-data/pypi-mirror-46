from game import *
from interface import RoadSelection
import numpy as np
FACTORY = {"KnightFactory": KnightFactory(), "ZombieFactory": ZombieFactory(), "PaladinFactory": PaladinFactory(), "WalkerFactory": WalkerFactory()}
KEYS = {113: 1, 119: 2, 101: 3, 114: 4}


class Event:
    def __init__(self):
        self.type = "none"


class PressEvent(Event):
    def __init__(self, x, y):
        super().__init__()
        self.type = "press"
        self.x = x
        self.y = y


class ReleaseEvent(Event):
    def __init__(self, x, y):
        super().__init__()
        self.type = "release"
        self.x = x
        self.y = y


class KeyPressEvent(Event):
    def __init__(self, symbol):
        super().__init__()
        self.type = "key_press"
        self.symbol = symbol


class Listener:
    def __init__(self):
        self.listening_for = []

    pass


class ButtonListener(Listener):
    def __init__(self, button_list):
        super().__init__()
        self.listening_for.append("press")
        self.listening_for.append("release")
        self.button_list = button_list

    def press(self, press_event: PressEvent):
        for button in self.button_list:
            if press_event.x > button.center_x + button.width / 2:
                continue
            if press_event.x < button.center_x - button.width / 2:
                continue
            if press_event.y > button.center_y + button.height / 2:
                continue
            if press_event.y < button.center_y - button.height / 2:
                continue
            button.on_press()

    def release(self, release_event: ReleaseEvent):
        for button in self.button_list:
            if button.pressed:
                button.on_release()


class KeyListener(Listener):
    def __init__(self, road_selection: RoadSelection, indicators_list, game: Game):
        super().__init__()
        self.game = game
        self.road_selection = road_selection
        self.indicators_list = indicators_list
        self.listening_for.append("key_press")

    def key_press(self, key_press_event: KeyPressEvent):
        if self.road_selection.selected_road == 0:
            if key_press_event.symbol == 49 or key_press_event.symbol == 50 or key_press_event.symbol == 51:
                self.road_selection.selected_road = key_press_event.symbol - 48
        else:
            if key_press_event.symbol == 49 or key_press_event.symbol == 50 or key_press_event.symbol == 51:
                if key_press_event.symbol - 48 == self.road_selection.selected_road:
                    self.road_selection.selected_road = 0
                else:
                    self.road_selection.selected_road = key_press_event.symbol - 48
            elif key_press_event.symbol in KEYS:
                    for i in self.indicators_list:
                        if i.key == KEYS[key_press_event.symbol]:
                            if i.on_choose():
                                    factory = FACTORY[i.unit_type + "Factory"]
                                    self.game.armies[0].add_unit(
                                        factory.create(x=300, y=int(SCREEN_HEIGHT *
                                                       (3 - self.road_selection.selected_road)/3 + SCREEN_HEIGHT/10
                                                       + np.random.sample()*SCREEN_HEIGHT/10),
                                                       road=self.road_selection.selected_road))
                                    self.road_selection.selected_road = 0



class ListenersSupport:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)

    def remove_listener(self, listener: Listener):
        self.listeners.remove(listener)

    def on_event(self, event: Event):
        for listener in self.listeners:
            if event.type in listener.listening_for:
                getattr(listener, event.type)(event)
