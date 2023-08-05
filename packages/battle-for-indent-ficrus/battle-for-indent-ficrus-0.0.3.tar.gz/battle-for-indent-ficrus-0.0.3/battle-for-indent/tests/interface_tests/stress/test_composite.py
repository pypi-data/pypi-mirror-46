"""
Тестируется способность модуля создать сложную composite-структуру (10^7 листьев),
а затем выполнить её полную отрисовку (вызов метода draw от каждого элемента)
"""

import interface

composite = interface.Composite()


def build_composite(root, depth):
    if depth < 6:
        for i in range(10):
            sub_composite = interface.Composite()
            root.add(sub_composite)

            build_composite(sub_composite, depth + 1)
    else:
        for i in range(10):
            root.add(interface.Leaf())


def test_build():
    try:
        build_composite(composite, 0)

        assert True
    except Exception:
        assert False


def test_leaf_count():
    assert len(composite.get_leaves()) == 10 ** 7


def test_draw():
    try:
        composite.draw()

        assert True
    except Exception:
        assert False
