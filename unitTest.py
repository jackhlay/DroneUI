import pytest
import tkinter as tk
from crud import CRUD  # Replace 'your_module_name' with the actual name of your module

@pytest.fixture
def app():
    root = tk.Tk()
    yield CRUD(root)
    root.destroy()

def test_add_item(app): #Code has now been written for this, but still fails
    app.entru.insert(0, "TestItem")
    app.add(app.entru.get())
    assert app.vList.size() == 1

def test_remove_item(app): #Code has now been written for this, but still fails
    app.vList.insert(tk.END, "TestItem")
    app.vList.selection_set(0)
    app.remove()
    assert app.vList.size() == 0