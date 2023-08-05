from abc import ABC

import arcade
from sprite import KnightSprite, ZombieSprite

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000


class Example(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate=1/60)

        self.player = KnightSprite(scale=0.25)
        self.zombie = ZombieSprite(scale=0.22)

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player.setup(300, 300)
        self.zombie.setup(500, 300)

    def on_draw(self):
        arcade.start_render()
        self.player.on_draw()
        self.zombie.on_draw()

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.zombie.move_left = True
        elif key == arcade.key.RIGHT:
            self.zombie.move_right = True
        elif key == arcade.key.W:
            self.zombie.attack = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.zombie.move_left = False
        if key == arcade.key.RIGHT:
            self.zombie.move_right = False
        if key == arcade.key.W:
            self.zombie.attack = False

    def update(self, delta_time):
        self.player.update(delta_time*60)
        self.zombie.update(delta_time*60)


def main():
    window = Example()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
