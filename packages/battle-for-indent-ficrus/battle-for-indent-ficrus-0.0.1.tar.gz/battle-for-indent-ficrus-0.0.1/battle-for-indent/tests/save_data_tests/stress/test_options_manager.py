"""
Тестируется работоспособность Options Manager при стрессовой нагрузке
"""

import time
from options_manager import OptionsManager

def profiler(func):
    def wrapper():
        start = time.time()

        func()

        finish = time.time()

        assert finish - start < 3
    return wrapper


@profiler
def test_many_openings():
    for i in range(10000):
        om = OptionsManager()


@profiler
def test_many_edits():
    value = OptionsManager().is_music_enabled
    other_value = OptionsManager().is_sounds_enabled
    for i in range(10000):
        OptionsManager().change_music()
        OptionsManager().change_sounds()

    assert value == OptionsManager().is_music_enabled
    assert other_value == OptionsManager().is_sounds_enabled


@profiler
def test_many_saves():
    for i in range(10000):
        OptionsManager().save_on_disk(OptionsManager().save())
