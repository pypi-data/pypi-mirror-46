import os
import units
from options_manager import OptionsManager
from progress_manager import ProgressManager
from event_handling import *


SCREEN_TITLE = "Battle for Indent"
TUTORIAL_TEXT = """
Welcome to Battle for Indent!
I'm a strange voice inside your head that will teach you how to play.

At first, you need to choose your fraction to fight for.

Then you should select units for the coming battle.
You can choose how much soldiers you will take.
Note, that number of units depepends on their power.

There are three roads on the battle map. Use 1, 2, 3 keys in order to choose suitable one.
Spawn unit on the selected road by pressing Q, W, E, R.

Good luck, King! Our victory is in your own hands.

WARNING! If you already have a save game, "Select Fraction" will erase it
"""
UNIT_SELECT_TEXT = """
Choose units for the battle.

Press
    Unit Name to see description
    - to remove unit
    Unit Count to zeroise it
    + to add unit

It's highly recommended to use as much Power, as you can.

Current Power: {0}
Max Power: {1}
"""


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True, update_rate=1/60)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.GRAY_BLUE)
        self.state = None

    def set_state(self, state=None):
        if state is None:
            self.state = MainMenuState(self)
        else:
            self.state = state

    def change_state(self, state):
        self.state = state

    def on_draw(self):
        arcade.start_render()
        self.state.on_draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.state.on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.state.on_mouse_release(x, y, button, key_modifiers)

    def update(self, delta_time: float):
        self.state.update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        self.state.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        self.state.on_key_release(symbol, modifiers)


class State:
    def __init__(self, window: Window):
        self.window = window

    def update(self, delta_time: float):
        pass

    def on_draw(self):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        pass


class MainMenuState(State):
    def __init__(self, window: Window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        game_buttons = Composite()
        self.gui.add(game_buttons)

        new_game_button = MenuButton(110, 480, 150, 50, "New Game", self.start_new_game)
        game_buttons.add(new_game_button)

        continue_button = MenuButton(110, 420, 150, 50, "Continue", self.continue_game)
        game_buttons.add(continue_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        options_button = MenuButton(110, 360, 150, 50, "Options", self.open_options)
        service_buttons.add(options_button)

        exit_button = MenuButton(110, 300, 150, 50, "Exit", self.exit_game)
        service_buttons.add(exit_button)

        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        self.gui.draw()

        arcade.draw_text("Start new game (with tutorial)\n", 200, 455, arcade.color.BLACK, 15)
        arcade.draw_text("Continue your game (if you have one)\n", 200, 395, arcade.color.BLACK, 15)
        arcade.draw_text("Change game options\n", 200, 335, arcade.color.BLACK, 15)
        arcade.draw_text("Exit game (please, no)\n", 200, 275, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def start_new_game(self):
        self.window.change_state(TutorialState(self.window))

    def continue_game(self):
        if ProgressManager().wins + ProgressManager().draws + ProgressManager().loses == 0:
            self.window.change_state(TutorialState(self.window))
        else:
            self.window.change_state(UnitSelectState(self.window))

    def open_options(self):
        self.window.change_state(OptionsState(self.window))

    def exit_game(self):
        exit(0)


class OptionsState(State):
    def __init__(self, window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None

        self.setup()

    def setup(self):
        om = OptionsManager()

        self.gui = Composite()
        self.listeners = ListenersSupport()

        option_buttons = Composite()
        self.gui.add(option_buttons)

        option1_button = MenuButton(110, 480, 150, 50, "{}".format(["Off", "On"][om.is_music_enabled]),
                                    self.change_music)
        option_buttons.add(option1_button)

        option2_button = MenuButton(110, 420, 150, 50, "{}".format(["Off", "On"][om.is_sounds_enabled]),
                                    self.change_sound)
        option_buttons.add(option2_button)

        option3_button = MenuButton(110, 360, 150, 50, "{}".format(["Off", "!!!PARTY!!!"][om.is_easter_egg_enabled]),
                                    self.change_egg)
        option_buttons.add(option3_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        return_button = MenuButton(110, 300, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)

    def on_draw(self):
        self.gui.draw()
        button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(button_list))

        arcade.draw_text("Background music (It may take some time to apply changes)\n", 200, 455, arcade.color.BLACK,
                         15)
        arcade.draw_text("Game sounds\n", 200, 395, arcade.color.BLACK, 15)
        arcade.draw_text("Use it if you aren't very serious\n", 200, 335, arcade.color.BLACK, 15)
        arcade.draw_text("Back to Main Menu\n", 200, 275, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def do_nothing(self):
        pass

    def update_options(self):
        self.window.change_state(OptionsState(self.window))

    def change_music(self):
        om = OptionsManager()
        om.change_music()

        self.update_options()

    def change_sound(self):
        om = OptionsManager()
        om.change_sounds()

        self.update_options()

    def change_egg(self):
        om = OptionsManager()
        om.change_egg()

        self.update_options()

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class TutorialState(State):
    def __init__(self, window: Window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        game_buttons = Composite()
        self.gui.add(game_buttons)

        unit_select_button = MenuButton(110, 480, 150, 50, "Select Fraction", self.fraction_select)
        game_buttons.add(unit_select_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        return_button = MenuButton(110, 420, 150, 50, "I'm not ready", self.return_to_menu)
        service_buttons.add(return_button)

        self.button_list = self.gui.get_leaves()
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        self.gui.draw()

        arcade.draw_text(TUTORIAL_TEXT, 200, 350, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def fraction_select(self) -> None:
        ProgressManager().reset()

        self.window.change_state(FractionSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class FractionSelectState(State):
    def __init__(self, window: Window):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None
        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        fractions_buttons = Composite()
        self.gui.add(fractions_buttons)

        spacers_select_button = MenuButton(110, 540, 150, 50, "Spacers", self.select_fraction, "Spacers")
        fractions_buttons.add(spacers_select_button)

        tabbers_select_button = MenuButton(110, 480, 150, 50, "Tabbers", self.select_fraction, "Tabbers")
        fractions_buttons.add(tabbers_select_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        return_button = MenuButton(110, 420, 150, 50, "I'm not ready", self.return_to_menu)
        service_buttons.add(return_button)

        self.button_list = self.gui.get_leaves()
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        self.gui.draw()

        arcade.draw_text("Fond of spaces. They use spaces, because they believe, that spaces came from Space Gods.\n", 200, 520, arcade.color.BLACK, 15)
        arcade.draw_text("Prefer using tabs everywhere, even in their everyday meals and speech.\n", 200, 460, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def select_fraction(self, fraction: str) -> None:
        ProgressManager().select_fraction(fraction)

        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class UnitSelectInfo:
    def __init__(self) -> None:
        self.current_power = 0
        self.max_power = 300 + ProgressManager().wins * 75 + ProgressManager().loses

        self.described_unit = None

        self.unit_count = {
            units.Knight: 0,
            units.Paladin: 0,
            units.Zombie: 0,
            units.Walker: 0
        }


class UnitSelectState(State):
    def __init__(self, window: Window, info=None):
        super().__init__(window)
        self.pause = False
        self.listeners = None
        self.gui = None
        self.parent = None

        if info is None:
            self._info = UnitSelectInfo()
        else:
            self._info = info

        self.setup()

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        knight_buttons = Composite()
        self.gui.add(knight_buttons)

        knight_button = MenuButton(110, 600, 150, 50, "Knight", self.show_unit_description, units.Knight)
        knight_buttons.add(knight_button)

        add_knight_button = MenuButton(260, 600, 50, 50, "-", self.remove_unit, units.Knight)
        knight_buttons.add(add_knight_button)

        knight_count_button = MenuButton(320, 600, 50, 50, "{}".format(self._info.unit_count[units.Knight]),
                                         self.clear_unit, units.Knight)
        knight_buttons.add(knight_count_button)

        remove_knight_button = MenuButton(380, 600, 50, 50, "+", self.add_unit, units.Knight)
        knight_buttons.add(remove_knight_button)

        zombie_buttons = Composite()
        self.gui.add(zombie_buttons)

        zombie_button = MenuButton(110, 540, 150, 50, "Zombie", self.show_unit_description, units.Zombie)
        zombie_buttons.add(zombie_button)

        add_zombie_button = MenuButton(260, 540, 50, 50, "-", self.remove_unit, units.Zombie)
        zombie_buttons.add(add_zombie_button)

        zombie_count_button = MenuButton(320, 540, 50, 50, "{}".format(self._info.unit_count[units.Zombie]),
                                         self.clear_unit, units.Zombie)
        zombie_buttons.add(zombie_count_button)

        remove_zombie_button = MenuButton(380, 540, 50, 50, "+", self.add_unit, units.Zombie)
        zombie_buttons.add(remove_zombie_button)

        paladin_buttons = Composite()
        self.gui.add(paladin_buttons)

        paladin_button = MenuButton(110, 480, 150, 50, "Paladin", self.show_unit_description, units.Paladin)
        paladin_buttons.add(paladin_button)

        if ProgressManager().wins > 0:
            add_paladin_button = MenuButton(260, 480, 50, 50, "-", self.remove_unit, units.Paladin)
            paladin_buttons.add(add_paladin_button)

            paladin_count_button = MenuButton(320, 480, 50, 50, "{}".format(self._info.unit_count[units.Paladin]),
                                                    self.clear_unit, units.Paladin)
            paladin_buttons.add(paladin_count_button)

            remove_paladin_button = MenuButton(380, 480, 50, 50, "+", self.add_unit, units.Paladin)
            paladin_buttons.add(remove_paladin_button)

        walker_buttons = Composite()
        self.gui.add(walker_buttons)

        walker_button = MenuButton(110, 420, 150, 50, "Walker", self.show_unit_description, units.Walker)
        walker_buttons.add(walker_button)

        if ProgressManager().wins > 1:
            add_walker_button = MenuButton(260, 420, 50, 50, "-", self.remove_unit, units.Walker)
            walker_buttons.add(add_walker_button)

            walker_count_button = MenuButton(320, 420, 50, 50, "{}".format(self._info.unit_count[units.Walker]),
                                                            self.clear_unit, units.Walker)
            walker_buttons.add(walker_count_button)

            remove_walker_button = MenuButton(380, 420, 50, 50, "+", self.add_unit, units.Walker)
            walker_buttons.add(remove_walker_button)

        service_buttons = Composite()
        self.gui.add(service_buttons)

        start_game_button = MenuButton(110, 360, 150, 50, "Start Game", self.start_game)
        service_buttons.add(start_game_button)

        return_button = MenuButton(110, 300, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)

        self.button_list = self.gui.get_leaves()
        self.listeners.add_listener(ButtonListener(self.button_list))

    def on_draw(self):
        self.gui.draw()

        if (self._info.described_unit) is not None:
            sprite = arcade.Sprite("../images/textures/{}.png".format(self._info.described_unit.__name__.lower()),
                                   center_x=550, center_y=375)
            sprite.draw()
            arcade.draw_text(units.get_decription(self._info.described_unit), 700, 275, arcade.color.BLACK, 15)

        arcade.draw_text(UNIT_SELECT_TEXT.format(self._info.current_power, self._info.max_power), 200, 650,
                         arcade.color.BLACK, 15)

        if ProgressManager().wins < 1:
            arcade.draw_text("Requires 1 win to hire\n", 200, 455, arcade.color.BLACK, 15)

        if ProgressManager().wins < 2:
            arcade.draw_text("Requires 2 wins to hire\n", 200, 395, arcade.color.BLACK, 15)

        arcade.draw_text("Start game with these units\n", 200, 335, arcade.color.BLACK, 15)
        arcade.draw_text("Back to Main Menu\n", 200, 275, arcade.color.BLACK, 15)

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def update(self, delta_time: float):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def do_nothing(self) -> None:
        pass

    def update_unit_select(self):
        self.window.change_state(UnitSelectState(self.window, self._info))

    def show_unit_description(self, UnitClass: units.BaseUnit) -> None:
        self._info.described_unit = UnitClass

        self.update_unit_select()

    def clear_unit(self, UnitClass: units.BaseUnit) -> None:
        self._info.current_power -= UnitClass().power * self._info.unit_count[UnitClass]
        self._info.unit_count[UnitClass] = 0

        self.update_unit_select()

    def add_unit(self, UnitClass: units.BaseUnit) -> None:
        if (self._info.current_power + UnitClass().power <= self._info.max_power):
            self._info.current_power += UnitClass().power
            self._info.unit_count[UnitClass] += 1
        else:
            pass

        self.update_unit_select()
    def remove_unit(self, UnitClass: units.BaseUnit) -> None:
        if (self._info.unit_count[UnitClass] > 0):
            self._info.current_power -= UnitClass().power
            self._info.unit_count[UnitClass] -= 1
        else:
            pass

        self.update_unit_select()

    def start_game(self) -> None:
        unit_dict = {UnitClass().job: self._info.unit_count[UnitClass] for UnitClass in self._info.unit_count}

        self.window.change_state(BattlefieldState(self.window, unit_dict))

    def unit_select(self) -> None:
        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


class BattlefieldState(State):
    def __init__(self, window: Window, unit_dict):
        super().__init__(window)
        self.unit_dict = unit_dict
        self.state = "Run"
        self.listeners = None
        self.run_listeners = None
        self.pause_listeners = None
        self.end_listeners = None
        self.run_gui = None
        self.pause_gui = None
        self.end_gui = None
        self.parent = None

        print(sum(value for key, value in unit_dict.items()))
        self.game = Game(max_cnt_1=sum(value for key, value in unit_dict.items()))
        self.game.player_max_units = sum([unit_dict[u] for u in unit_dict])

        self.setup()

    def setup(self):
        self.run_setup()
        self.pause_setup()
        self.victory_setup()
        self.listeners = self.run_listeners

    def run_setup(self):
        self.run_gui = Composite()
        self.run_listeners = ListenersSupport()
        self.run_gui.add(Stage("../images/stage/stage-back.png"))
        self.run_gui.add(self.game.gui)
        road_selection = RoadSelection()
        self.run_gui.add(road_selection)
        cooldown_indicators = Composite()
        self.run_gui.add(cooldown_indicators)

        x = 100
        y = 100
        width = 100
        height = 100
        key = 1

        cooldown_indicators_list = []
        for k, value in self.unit_dict.items():
            cooldown_indicator = CooldownIndicator(x, y, width, height, k, value, 10, key)
            cooldown_indicators.add(cooldown_indicator)
            x += width + 10
            key += 1
            cooldown_indicators_list.append(cooldown_indicator)
        key_listener = KeyListener(road_selection, cooldown_indicators_list, self.game)
        self.run_listeners.add_listener(key_listener)
        self.run_gui.add(Stage("../images/stage/stage-front.png"))
        buttons = Composite()
        self.run_gui.add(buttons)

        pause_button = MenuButton(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50, 50, 50, " || ", self.pause_game)
        buttons.add(pause_button)
        button_list = [button for button in self.run_gui.get_leaves() if isinstance(button, Button)]
        self.run_listeners.add_listener(ButtonListener(button_list))

    def pause_setup(self):
        self.pause_gui = Composite()
        self.pause_gui.add(Image(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8, 0.25, "../images/textures/gray.png"))
        self.pause_listeners = ListenersSupport()

        game_buttons = Composite()
        self.pause_gui.add(game_buttons)

        continue_button = MenuButton(SCREEN_WIDTH/2, SCREEN_HEIGHT*7/8 + 85, 150, 50, "Continue", self.continue_game)
        game_buttons.add(continue_button)

        restart_button = MenuButton(SCREEN_WIDTH/2, SCREEN_HEIGHT*7/8 + 25, 150, 50, "Restart", self.restart_game)
        game_buttons.add(restart_button)

        service_buttons = Composite()
        self.pause_gui.add(service_buttons)

        return_button = MenuButton(SCREEN_WIDTH/2, SCREEN_HEIGHT*7/8 - 35, 150, 50, "Return", self.return_to_menu)
        service_buttons.add(return_button)
        button_list = [button for button in self.pause_gui.get_leaves() if isinstance(button, Button)]
        self.pause_listeners.add_listener(ButtonListener(button_list))

    def victory_setup(self):
        self.end_gui = Composite()
        self.end_gui.add(Image(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 7 / 8, 0.25, "../images/textures/gray.png"))
        self.end_listeners = ListenersSupport()
        game_buttons = Composite()
        self.end_gui.add(game_buttons)

        restart_button = MenuButton(SCREEN_WIDTH/2, SCREEN_HEIGHT*7/8 + 25, 175, 50, "New battle", self.restart_game)
        game_buttons.add(restart_button)

        return_button = MenuButton(SCREEN_WIDTH/2,  SCREEN_HEIGHT*7/8 - 35, 175, 50, "Return to menu", self.return_to_menu)
        game_buttons.add(return_button)
        button_list = [button for button in self.end_gui.get_leaves() if isinstance(button, Button)]
        self.end_listeners.add_listener(ButtonListener(button_list))


    def on_draw(self):
        self.run_gui.draw()
        if self.state == 'Pause':
            self.pause_gui.draw()
        elif self.state == 'End':
            self.end_gui.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.listeners.on_event(PressEvent(x, y))

    def on_mouse_release(self, x, y, button, key_modifiers):
        self.listeners.on_event(ReleaseEvent(x, y))

    def on_key_press(self, symbol: int, modifiers: int):
        if self.state == 'Run':
            self.listeners.on_event(KeyPressEvent(symbol))

    def update(self, delta_time: float):
        if self.state == 'Run':
            self.run_gui.update(delta_time)

            value = self.game.update()
            if value == 1:
                self.win_game()
            elif value == 2:
                self.lose_game()
            elif value == 3:
                self.draw_game()


    def end_game(self, result):
        r_dict = {1: "Victory", 2: "Lose", 3: "Draw"}
        self.state = 'End'
        self.listeners = self.end_listeners
        self.end_gui.add(Text(r_dict[result], SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT*7/8 + 75))

        end_text = ["King of {} brought army to victory!\n".format(ProgressManager().fraction),
                    "Not the best day for {}, King...\n".format(ProgressManager().fraction),
                    "Friendship won? No, never!\n"][result - 1]

        self.end_gui.add(Text(end_text, SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT*7/8 - 100, arcade.color.BLACK, 15))
        
    def win_game(self):
        ProgressManager().add_win()

        self.end_game(1)

    def lose_game(self):
        ProgressManager().add_lose()

        self.end_game(2)

    def draw_game(self):
        ProgressManager().add_draw()

        self.end_game(3)

    def pause_game(self):
        self.state = 'Pause'
        self.listeners = self.pause_listeners

    def continue_game(self):
        self.state = 'Run'
        self.listeners = self.run_listeners

    def restart_game(self):
        self.window.change_state(UnitSelectState(self.window))

    def return_to_menu(self) -> None:
        self.window.change_state(MainMenuState(self.window))


def play_music_once(*args):
    if OptionsManager().is_music_enabled:
        music = arcade.load_sound("../sounds/main-menu-theme.wav")
        arcade.play_sound(music)


def play_music():
    play_music_once()
    arcade.schedule(play_music_once, 22)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.set_state(MainMenuState(window))

    play_music()

    arcade.run()
