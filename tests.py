import pytest
from unittest.mock import Mock
from MVC import Model

@pytest.fixture
def mock_observer():
    return Mock()

def test_initialization():
    model = Model()
    assert model.coordinates == []

def test_add_coordinate():
    model = Model()
    model.add_coordinate(1, 2)
    assert model.coordinates == [(1, 2)]

def test_add_multiple_coordinates():
    model = Model()
    model.add_coordinate(1, 2)
    model.add_coordinate(3, 4)
    assert model.coordinates == [(1, 2), (3, 4)]

def test_register_observer(mock_observer):
    model = Model()
    model.register_observer(mock_observer)
    assert mock_observer in model.observers

def test_notify_observers(mock_observer):
    model = Model()
    model.register_observer(mock_observer)
    model.add_coordinate(1, 2)
    mock_observer.update_view.assert_called_once_with([(1, 2)])

def test_generate_plan(): #we do not use this generate_plan function, so easy free test
    model = Model()
    model.add_coordinate(1, 2)
    model.add_coordinate(3, 4)
    assert model.generate_plan() == None

def test_generate_plan_empty(): #consistency
    model = Model()
    assert model.generate_plan() == None

def test_notify_observers_empty(mock_observer): 
    model = Model()
    model.register_observer(mock_observer)
    model.notify_observers()
    mock_observer.update_view.assert_called_once_with([])

def test_add_same_coordinate(): #you are allowed to add the same coordinate as many times as you want
    model = Model()
    model.add_coordinate(1, 2)
    model.add_coordinate(1, 2)
    assert model.coordinates == [(1, 2), (1, 2)]

def test_notify_multiple_observers():
    model = Model()
    observer1 = Mock()
    observer2 = Mock()
    model.register_observer(observer1)
    model.register_observer(observer2)
    model.add_coordinate(1, 2)
    observer1.update_view.assert_called_once_with([(1, 2)])
    observer2.update_view.assert_called_once_with([(1, 2)])
