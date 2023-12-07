import tkinter as tk
from tkintermapview import TkinterMapView

class SingletonRoot(tk.Tk):
    _instance = None #static my instance singleton

    def __new__(cls): #instantiating/checking for existing instance
        if cls._instance is None:
            cls._instance = super(SingletonRoot, cls).__new__(cls)
        return cls._instance

    def initialize(self): #making new instance
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.geometry("360x480")
            self.title("Coordinate App")
            self.resizable(width=False, height=False)

class Model():
    def __init__(self):
        self.coordinates = []
        self.observers = []

    def add_coordinate(self, latitude, longitude):
        self.coordinates.append((latitude, longitude))
        self.notify_observers()

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update_view(self.coordinates)

    def generate_plan(self):
        print("Generating plan with coordinates:", self.coordinates)

class View: #ugly view monolith

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.controller.model.register_observer(self)
        self.root.geometry("360x480")  # Initial size, adjust as needed
        self.root.title("Coordinate App")
        self.root.resizable(width=False, height=False)

        def center_map():
            print(self.address_entry.get())
            self.map_view.set_address(self.address_entry.get())

        def remove():
            print("selected: ", self.vList.curselection()[0])
            self.vList.delete(self.vList.curselection()[0])

        # Configure column and row weights for centerin

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.vList = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.vList.grid(row=2, column=0, columnspan=3, sticky="e")

        self.entry = tk.Entry(root)

        self.removeButton = tk.Button(root, text="Remove", command=remove)
        self.removeButton.grid(row=3, column=0, columnspan=3, sticky="e")

        self.address_label = tk.Label(root, text="Address")
        self.address_label.grid(row=1, column=0, sticky="w")

        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=1, column=1, columnspan=3, sticky="w")

        self.add_button = tk.Button(root, text="enter", command=center_map)
        self.add_button.grid(row=1, column =3, columnspan=1, sticky="nesw")

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, sticky = "nesw")

        self.generate_button = tk.Button(root, text="Fly", command=controller.fly_button_pressed)
        self.generate_button.grid(row=7, column=1, columnspan=2, sticky="w")

        self.map_view = TkinterMapView(root, width=360, height=250, corner_radius=3)
        self.map_view.grid(row=8, columnspan=3, sticky="nsew")
        self.map_view.set_zoom(20)

        def add_coords(coords):
            print("Added coords:", coords)
            self.vList.insert(tk.END, coords)
            self.controller.add_coordinates(coords[0], coords[1])
            new_marker = self.map_view.set_marker(coords[0], coords[1], text="")
    

        self.map_view.add_right_click_menu_command(label="Add coords",
                                        command=add_coords,
                                        pass_coords=True)

        # Expand all columns and rows
        self.root.rowconfigure(8, weight=1)
        for i in range(3):
            self.root.columnconfigure(i, weight=1)

    def update_view(self, coordinates):
        self.vList.delete(0, tk.END)  # Clear the Listbox
        for coord in coordinates:
            self.vList.insert(tk.END, coord)

class Controller:

    def __init__(self, root):
        self.planArr = []
        self.model = Model()
        self.view = View(root, self)

    def add_coordinates(self, lat, lon):
        self.model.add_coordinate(lat, lon)
        self.view.result_label.config(text="Coordinates added successfully.")
            
    def generate_plan(self):
        self.planArr.extend(self.model.coordinates)
        self.view.result_label.configure(text="Plan generated!")
        return self.planArr
    
    def fly_button_pressed(self):
        self.generate_plan()
        self.root.destroy()

if __name__ == "__main__":
    root = SingletonRoot()
    app = Controller(root)
    root.mainloop()
    root.quit()
