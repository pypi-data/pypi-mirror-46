from state import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RELEASE_COUNT = 200

gui = Composite()
listeners = ListenersSupport()


class Count:
    def __init__(self):
        self.count = 0

    def increase(self):
        self.count += 1

    def clear(self):
        self.count = 0


count = Count()

button_coords = {"new_game": [110, 480, 150, 50], "continue": [110, 420, 150, 50],
                 "options": [110, 360, 150, 50], "exit": [110, 300, 150, 50]}

game_buttons = Composite()
gui.add(game_buttons)

new_game_button = MenuButton(button_coords["new_game"][0], button_coords["new_game"][1],
                             button_coords["new_game"][2], button_coords["new_game"][3],
                             "New Game", count.increase)
game_buttons.add(new_game_button)

continue_button = MenuButton(button_coords["continue"][0], button_coords["continue"][1],
                             button_coords["continue"][2], button_coords["continue"][3],
                             "Continue", count.increase)
game_buttons.add(continue_button)

service_buttons = Composite()
gui.add(service_buttons)

options_button = MenuButton(button_coords["options"][0], button_coords["options"][1],
                            button_coords["options"][2], button_coords["options"][3],
                            "Options", count.increase)
service_buttons.add(options_button)

exit_button = MenuButton(button_coords["exit"][0], button_coords["exit"][1],
                         button_coords["exit"][2], button_coords["exit"][3],
                         "Exit", count.increase)
service_buttons.add(exit_button)

button_list = [button for button in gui.get_leaves() if isinstance(button, Button)]
listeners.add_listener(ButtonListener(button_list))


def test_raise_press_and_release():
    xs = np.random.rand(RELEASE_COUNT) * SCREEN_WIDTH
    ys = np.random.rand(RELEASE_COUNT) * SCREEN_HEIGHT
    check_count = 0
    count.clear()
    for i in range(RELEASE_COUNT):
        press_event = PressEvent(xs[i], ys[i])
        listeners.on_event(press_event)
        release_event = ReleaseEvent(xs[i], ys[i])
        listeners.on_event(release_event)
        for button in button_list:
            if press_event.x > button.center_x + button.width / 2:
                continue
            if press_event.x < button.center_x - button.width / 2:
                continue
            if press_event.y > button.center_y + button.height / 2:
                continue
            if press_event.y < button.center_y - button.height / 2:
                continue
            check_count += 1
    assert check_count == count.count

