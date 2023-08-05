"""
Тестируется способность отрисовать анимацию 200 рыцарей (1600 объектов) одновременно
"""

from tests.animation_tests.base_animation import *
RUN_TIME = 10


def test_simple_animation():
    window = SimpleAnimationTest(count_knights=200)
    window.setup()
    window.test(60 * RUN_TIME)
    assert (window.time >= RUN_TIME - 1)
    window.close()


class SimpleAnimationTest(AnimationTest):
    def __init__(self, count_knights):
        super().__init__(count_knights)

    def update(self, delta_time):
            self.time += delta_time
            if self.time < 1:
                pass
            else:
                assert True
                for player in self.players:
                    player.update(delta_time * 60)
                    if player.move_right:
                        if player.center_x < SCREEN_WIDTH - 500:
                            pass
                        else:
                            player.move_right = False
                            player.move_left = True
                    if player.move_left:
                        if player.center_x > 200:
                            pass
                        else:
                            player.move_left = False
                            player.move_right = True
