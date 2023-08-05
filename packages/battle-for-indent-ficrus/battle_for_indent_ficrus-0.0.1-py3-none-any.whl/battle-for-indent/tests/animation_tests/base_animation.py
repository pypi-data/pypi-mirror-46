import random
import arcade
from sprite import KnightSprite
from tests.animation_tests.animation_of_character import SCREEN_WIDTH, SCREEN_HEIGHT


class AnimationTest(arcade.Window):

    def __init__(self, count_knights):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate=1/60)
        self.players = []
        for i in range(count_knights):
            self.players.append(KnightSprite(scale=0.25))

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.LIGHT_GREEN)
        self.time = 0

    def setup(self):
        for player in self.players:
            player.setup(300 + int(random.random()*500), 300 + int(random.random()*500))
            player.move_right = True

    def on_draw(self):
        arcade.start_render()
        for player in self.players:
            player.on_draw()

    def update(self, delta_time):
        pass


