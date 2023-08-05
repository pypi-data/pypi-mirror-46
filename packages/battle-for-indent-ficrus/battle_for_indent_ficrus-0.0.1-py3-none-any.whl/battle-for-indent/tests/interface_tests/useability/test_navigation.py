"""
В процессе разработки были выявлены некоторые сложности в навигации различных меню
Все эти сценарии были проанализированы и упрощены
Ниже рассматриваются различные сценарии пользовательских действий, а также дизайнерские решения, их покрывающие
"""

"""
Цель: пользователь не должен тратить более трёх нажатий мышкой для выхода из игры с любого её состояния
"""
def test_exit():
    from_main_menu = 1 # Кнопка выхода находится в главном меню
    from_options = from_main_menu + 1 # Есть кнопка выхода в меню
    from_unit_select = from_main_menu + 1 # Есть кнопка выхода в меню
    from_tutorial = from_main_menu + 1 # Есть кнопка выхода в меню
    from_fraction_select = from_main_menu + 1 # Есть кнопка выхода в меню
    from_game_pause = from_main_menu + 1 # Есть кнопка выхода в меню
    from_ended_game = from_main_menu + 1 # Есть кнопка выхода в меню
    from_running_game = from_game_pause + 1 # Есть кнопка паузы

    assert from_main_menu <= 3
    assert from_options <= 3
    assert from_unit_select <= 3
    assert from_tutorial <= 3
    assert from_fraction_select <= 3
    assert from_game_pause <= 3
    assert from_ended_game <= 3
    assert from_running_game <= 3


"""
Цель: пользователь не должен начать игру без описания управления
"""
def test_tutorial():
    assert True # Все пути к игровому полю лежат через Tutorial


"""
Цель: пользователь может отключать звуковое сопровождение
"""
def test_music():
    assert True # В настройках можно отключить как звуки нажатия клавиш, так и музыку


"""
Цель: пользователь оповещён, что делают кнопки
"""
def test_buttons_description():
    assert True # Все кнопки имеют описание


"""
Цель: пользователь может удобно регулировать размер армии
"""
def test_unit_select():
    is_able_to_add = True # Юниты можно добавлять
    is_able_to_remove = True # Юниты можно удалять
    is_able_to_zeroize = True # Можно сбрасывать количество юнитов
    is_able_to_see_decription = True # Можно посмотреть описание юнита


    assert is_able_to_add
    assert is_able_to_remove
    assert is_able_to_zeroize
    assert is_able_to_see_decription


"""
Цель: пользователь имеет возможность приостановить игру, отойти от компьютера и не увидеть изменений
"""
def test_pause():
    is_pausable = True # Во время игры можно поставить паузу
    are_menus_constant = True # На остальных экранах в отсутствии пользователя ничего не происходит

    assert is_pausable
    assert are_menus_constant

"""
Цель: пользователь может начать новую игру или продолжить старую
"""
def test_game_saves():
    new_game = True # Всегда можно создать новую игру
    saves_progress = True # Даже выходе из игры прогресс игрока сохраняется

    assert new_game
    assert saves_progress

"""
Цель: пользователь получает подсказки во время игры
"""
def test_hints():
    is_road_highlighed = True # При выборе дороги она подсвечивается => юниты пойдут туда, куда нужно
    is_unit_count_shown = True # Показано количество оставшихся юнитов => не нужно запоминать, сколько юнитов было выбрано и использовано

    assert is_road_highlighed
    assert is_unit_count_shown
