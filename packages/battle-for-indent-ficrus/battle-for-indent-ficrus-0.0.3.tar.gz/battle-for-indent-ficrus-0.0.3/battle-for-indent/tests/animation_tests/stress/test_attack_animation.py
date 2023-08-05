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
        self.cnt = 0

    def setup(self):
        super().setup()
        for player in self.players:
            player.move_right = False

    def update(self, delta_time):
            self.time += delta_time
            if self.time < 1:
                pass
            else:
                assert True
                if self.cnt < 3:
                    b = False
                    for player in self.players:

                        if not player.start_attack:
                            if not b:
                                b = True
                            player.attack = True
                    if b:
                        self.cnt += 1
                for player in self.players:
                    player.update(delta_time * 60)
