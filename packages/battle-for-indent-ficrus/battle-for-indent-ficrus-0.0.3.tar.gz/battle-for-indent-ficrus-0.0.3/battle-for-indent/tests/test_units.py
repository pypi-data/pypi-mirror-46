import units

knight = units.Knight()
another_knight = units.Knight()

zombie = units.Zombie()
another_zombie = units.Zombie()


def test_inheritance():
    assert isinstance(knight, units.BaseUnit) is True
    assert isinstance(zombie, units.BaseUnit) is True


def test_difference():
    assert (knight is another_knight) is False
    assert (zombie is another_zombie) is False
    assert (knight is zombie) is False


def test_creation():
    assert knight.job == "Knight"
    assert zombie.job == "Zombie"

    assert knight.hp != 0
    assert zombie.hp != 0


def test_attack():
    health_before = zombie.hp
    knight.attack(zombie)
    health_after = zombie.hp

    assert health_after != health_before
    assert health_after != another_zombie.hp
