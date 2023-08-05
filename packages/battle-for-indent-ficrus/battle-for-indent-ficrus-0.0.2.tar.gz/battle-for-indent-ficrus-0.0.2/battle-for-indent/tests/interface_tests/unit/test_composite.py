import interface

composite = interface.Composite()
another_composite = interface.Composite()

leaf = interface.Leaf()
another_leaf = interface.Leaf()


def test_inheritance():
    assert isinstance(composite, interface.Component) is True
    assert isinstance(another_composite, interface.Component) is True

    assert isinstance(leaf, interface.Component) is True
    assert isinstance(another_leaf, interface.Component) is True


def test_difference():
    assert (composite is another_composite) is False
    assert (leaf is another_leaf) is False
    assert (composite is leaf) is False


def test_type():
    assert composite.is_composite() is True
    assert leaf.is_composite() is False


def test_add_remove():
    composite.add(leaf)
    composite.remove(leaf)


def test_get_leaves():
    assert leaf.get_leaves() == []
    assert leaf.get_all_elements() == []
    assert composite.get_leaves() == []

    composite.add(leaf)
    father_composite =  interface.Composite()
    father_composite.add(composite)

    assert set(father_composite.get_all_elements()) == set([leaf, composite])
    assert father_composite.get_leaves() == [leaf]

    composite.remove(leaf)
