"""
Тестируется работоспособность Options Manager при высокой нагрузке
"""

import time
from options_manager import OptionsManager

def profiler(func):
    def wrapper():
        start = time.time()

        func()

        finish = time.time()

        assert finish - start < 1
    return wrapper


@profiler
def test_many_openings():
    for i in range(100):
        om = OptionsManager()


@profiler
def test_many_edits():
    value = OptionsManager().is_music_enabled
    other_value = OptionsManager().is_sounds_enabled
    for i in range(100):
        OptionsManager().change_music()
        OptionsManager().change_sounds()

    assert value == OptionsManager().is_music_enabled
    assert other_value == OptionsManager().is_sounds_enabled


@profiler
def test_many_saves():
    for i in range(100):
        OptionsManager().save_on_disk(OptionsManager().save())
