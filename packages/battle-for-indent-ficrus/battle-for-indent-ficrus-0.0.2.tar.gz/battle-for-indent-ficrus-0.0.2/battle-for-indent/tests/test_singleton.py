import unit_factories


knight_factory = unit_factories.KnightFactory()
second_knight_factory = unit_factories.KnightFactory()
zombie_factory = unit_factories.ZombieFactory()


def test_similar_factories():
    assert (knight_factory is second_knight_factory) is True


def test_different_factories():
    assert (knight_factory is zombie_factory) is False
