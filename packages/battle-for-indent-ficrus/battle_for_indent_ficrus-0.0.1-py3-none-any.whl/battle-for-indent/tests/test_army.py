from army import Army
import unit_factories

knight_factory = unit_factories.KnightFactory()
knight = knight_factory.create()
zombie_factory = unit_factories.ZombieFactory()
zombie = zombie_factory.create()
army1 = Army()
army2 = Army()
army2.add_unit(knight)
army3 = Army()
army3.add_unit(knight)
army3.add_unit(zombie)


def test_empty():
    assert (army1.units.get_leaves() == []) is True


def test_one():
    assert (len(army2.units.get_leaves()) == 1) is True


def test_two():
    assert (len(army3.units.get_leaves()) == 2) is True


def test_difference():
    assert (army1.units is army2.units) is False
