"""
Тестируется реакция нескольких объектов на нажатия одновременно,
 в том числе и когда объекты пересекаются в момент нажатия
"""

from state import *


COUNT = 2000
BUTTON_NUM = 4
PAUSE = 1
RUN_TIME = 10
BUTTON_SETTINGS = {"lower_w": SCREEN_WIDTH/16, "lower_h": SCREEN_HEIGHT/16, "upper_w": SCREEN_WIDTH*3/16, "upper_h": SCREEN_HEIGHT*3/16, "max_speed": 20}


class PressChecker:
    def __init__(self, state, x, y, width, height, num):
        self.state = state
        self.xs = list(np.random.rand(num) * width + x)
        self.ys = list(np.random.rand(num) * height + y)
        self.time = list(np.random.rand(num) * RUN_TIME)
        self.pressed = list([False] * num)
        self.released = list([False] * num)
        self.num = num
        self.count = 0
        self.button_pressed = list([False]*len(self.state.button_list))

    def raise_press(self):
        for i in range(self.num):
            if self.time[i] <= self.state.TIME and self.pressed[i] is False:
                self.state.on_mouse_press(self.xs[i], self.ys[i], 0, None)
                self.pressed[i] = True
                for j in range(len(self.state.button_list)):
                    button = self.state.button_list[j]
                    if self.xs[i] > button.center_x + button.width / 2:
                        continue
                    if self.xs[i] < button.center_x - button.width / 2:
                        continue
                    if self.ys[i] > button.center_y + button.height / 2:
                        continue
                    if self.ys[i] < button.center_y - button.height / 2:
                        continue
                    self.button_pressed[j] = True
            if self.time[i] + PAUSE <= self.state.TIME and self.released[i] is False:
                self.state.on_mouse_release(self.xs[i], self.ys[i], 0, None)
                for j in range(len(self.state.button_list)):
                    if self.button_pressed[j] is True:
                        self.count += 1
                        self.button_pressed[j] = False
                self.released[i] = True

    def check(self):
        assert self.state.count == self.count


class TesState(MainMenuState):
    def __init__(self, window):
        super().__init__(window)
        self.count = 0
        self.TIME = 0
        self.press_checker = PressChecker(self, 35, 300, 150, 180, COUNT)

    def set_press_checker(self, press_checker):
        self.press_checker = press_checker

    def update(self, delta_time: float):
        self.TIME += delta_time
        self.press_checker.raise_press()
        self.press_checker.check()
        if self.TIME > RUN_TIME:
            arcade.quick_run(1)

    def start_new_game(self):
        self.count += 1

    def continue_game(self):
        self.count += 1

    def open_options(self):
        self.count += 1

    def exit_game(self):
        self.count += 1

    def on_draw(self):
        self.gui.draw()


class MovingButton(MenuButton):
    def __init__(self, center_x, center_y, width, height, text, action_function, speed_x=0, speed_y=0):
        super().__init__(center_x, center_y, width, height, text, action_function)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, timedelta):
        self.center_x += self.speed_x * timedelta
        self.center_y += self.speed_y * timedelta
        if self.center_x + self.width/2 >= SCREEN_WIDTH or self.center_x - self.width/2 <= 0:
            self.speed_x = - self.speed_x
        if self.center_y + self.height/2 >= SCREEN_HEIGHT or self.center_y - self.height/2 <= 0:
            self.speed_y = - self.speed_y


class UTestState(TesState):
    def __init__(self, window, num_buttons, button_settings):
        self.num_buttons = num_buttons
        self.button_settings = button_settings
        super().__init__(window)

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        game_buttons = Composite()
        self.gui.add(game_buttons)
        for i in range(self.num_buttons):
            width = int(np.random.sample()*self.button_settings["upper_w"]+self.button_settings["lower_w"])
            height = int(np.random.sample() * self.button_settings["upper_h"] + self.button_settings["lower_h"])
            button = MovingButton(int(np.random.sample()*(SCREEN_WIDTH - width) + width/2),
                                  int(np.random.sample()*(SCREEN_HEIGHT - height) + height/2),
                                  width, height, "aaaaa", self.start_new_game,
                                  int(-self.button_settings["max_speed"] + self.button_settings["max_speed"]*np.random.sample()*2),
                                  int(-self.button_settings["max_speed"] + self.button_settings["max_speed"]*np.random.sample()*2))
            game_buttons.add(button)

        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, MovingButton)]
        self.listeners.add_listener(ButtonListener(self.button_list))

    def update(self, delta_time: float):
        super().update(delta_time)
        for button in self.button_list:
            button.update(delta_time)


def test_presses_and_releases_everywhere():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    state = UTestState(window, BUTTON_NUM, BUTTON_SETTINGS)
    state.set_press_checker(PressChecker(state, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, COUNT))
    window.set_state(state)
    window.test(60 * RUN_TIME)
    window.close()

