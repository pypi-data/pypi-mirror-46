"""
Тестируется реакция нескольких объектов на нажатия одновременно
"""
from state import *


COUNT = 10
SQRT_BUTTON_NUM = 2
PAUSE = 1
RUN_TIME = 2


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


class StressTestState(TesState):
    def __init__(self, window, sqrt_num_buttons):
        self.sqrt_num_buttons = sqrt_num_buttons
        super().__init__(window)

    def setup(self):
        self.gui = Composite()
        self.listeners = ListenersSupport()

        game_buttons = Composite()
        self.gui.add(game_buttons)
        for i in range(self.sqrt_num_buttons):
            for j in range(self.sqrt_num_buttons):
                width = int(SCREEN_WIDTH/SQRT_BUTTON_NUM)
                height = int(SCREEN_HEIGHT/SQRT_BUTTON_NUM)
                button = MenuButton(i*width + width/2,
                                    j*height + height/2,
                                    width, height, str(i + j * SQRT_BUTTON_NUM), self.start_new_game)
                game_buttons.add(button)
        self.button_list = [button for button in self.gui.get_leaves() if isinstance(button, Button)]
        self.listeners.add_listener(ButtonListener(self.button_list))


def test_presses_and_releases_everywhere():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    state = StressTestState(window, SQRT_BUTTON_NUM)
    state.set_press_checker(PressChecker(state, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, COUNT))
    window.set_state(state)
    window.test(60 * RUN_TIME)
    window.close()

