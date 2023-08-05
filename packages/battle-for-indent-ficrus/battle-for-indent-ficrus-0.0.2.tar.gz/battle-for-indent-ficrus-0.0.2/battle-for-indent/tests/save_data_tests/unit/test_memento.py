"""
Теструются базовые требования паттерна Memento
"""

from abc import ABC, abstractmethod
from datetime import datetime
import memento


class Owner:
    def __init__(self, additional_data=None):
        self.a = 1
        self.b = 2
        self.additional_data = additional_data

    def save(self):
        return OwnedMemento([self.a,
                             self.b,
                             self.additional_data])

    def restore(self, memento):
        (self.a,
        self.b,
        self.additional_data) = memento.get_state()

    def change_a(self, new_a):
        self.a = new_a


class OwnedMemento(memento.Memento):
    def __init__(self, state: list) -> None:
        self._state = state
        self._date = str(datetime.now())

    def get_state(self) -> list:
        return self._state

    def get_name(self) -> str:
        return f"{self._date} / ({self._state[0:9]}...)"

    def get_date(self) -> str:
        return self._date


owner = Owner()
another_owner = Owner()
owner_with_data = Owner("Remember Me")

owners_memento = owner.save()
another_owners_memento = another_owner.save()
last_memento = owner_with_data.save()


def test_inheritance():
    assert isinstance(owners_memento, memento.Memento)
    assert isinstance(another_owners_memento, memento.Memento)
    assert isinstance(last_memento, memento.Memento)


def test_difference():
    assert (owner is another_owner) is False
    assert (owner is owner_with_data) is False
    assert (owners_memento is another_owners_memento) is False
    assert (owners_memento is last_memento) is False


def test_restore_with_no_changes():
    temp = Owner()
    temp.a = owner.a
    temp.b = owner.b
    temp.additional_data = owner.additional_data

    owner.restore(owners_memento)
    
    assert temp.a == owner.a
    assert temp.b == owner.b
    assert temp.additional_data == owner.additional_data


def test_restore_with_full_change():
    temp = Owner()
    temp.a = another_owner.a
    temp.b = another_owner.b
    temp.additional_data = another_owner.additional_data

    another_owner.a = 100500
    another_owner.b = 1337
    another_owner.additional_data = "+inf"

    another_owner.restore(another_owners_memento)

    assert temp.a == another_owner.a
    assert temp.b == another_owner.b
    assert temp.additional_data == another_owner.additional_data


def test_two_mementos():
    new_memento = owner.save()

    assert (new_memento is owners_memento) is False
    assert new_memento.get_date() != owners_memento.get_date()
    assert new_memento.get_state() == owners_memento.get_state()


def test_access():
    try:
        some_data = owners_memento._state
        assert False
    except Exception as e:
        assert True


def test_change():
    temp = owner.a
    owner.change_a(20000)

    owner.restore(owners_memento)

    assert temp == owner.a
