import unit_factories

knight_factory = unit_factories.KnightFactory()
first_knight = knight_factory.create()
second_knight = knight_factory.create()
zombie_factory = unit_factories.ZombieFactory()
first_zombie = zombie_factory.create()
second_zombie = zombie_factory.create()


def test_knight_difference():
    assert (first_knight is second_knight) is False


def test_bandit_difference():
    assert (first_zombie is second_zombie) is False


def test_knight_class():
    assert (first_knight.__class__ is unit_factories.Knight) is True


def test_bandit_class():
    assert (first_zombie.__class__ is unit_factories.Zombie) is True
