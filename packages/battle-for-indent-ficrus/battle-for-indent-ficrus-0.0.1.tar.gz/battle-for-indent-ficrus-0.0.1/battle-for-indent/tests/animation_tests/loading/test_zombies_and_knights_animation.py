"""
Тестируется способность отрисовать анимацию 30 рыцарей и 30 зомби одновременно
"""

from tests.animation_tests.base_animation import *
from sprite import ZombieSprite
RUN_TIME = 6


def test_simple_animation():
    window = ZombieandKnightAnimationTest(count_knights=30, count_zombies=30)
    window.setup()
    window.test(60 * RUN_TIME)
    assert (window.time >= RUN_TIME - 1)
    window.close()


class ZombieandKnightAnimationTest(AnimationTest):
    def __init__(self, count_knights, count_zombies):
        super().__init__(count_knights)
        for i in range(count_zombies):
            self.players.append(ZombieSprite(scale=0.25))

    def setup(self):
        for player in self.players:
            if type(player).__name__ == 'KnightSprite':
                player.setup(int(random.random()*250), 400 + int(random.random()*250))
                player.move_right = True
            else:
                player.setup(SCREEN_WIDTH - 550 + int(random.random() * 250), 400 + int(random.random() * 250))
                player.move_left = True

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
