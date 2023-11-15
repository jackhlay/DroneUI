import tkinter as tk

class Model:
    def __init__(self):
        self.coordinates = []

    def add_coordinate(self, latitude, longitude):
        self.coordinates.append((latitude, longitude))

    def generate_plan(self):
        print("Generating plan with coordinates:", self.coordinates)

class View: #ugly view monolith

    def __init__(self, root, controller):
        self.root = root
        self.root.geometry("360x480")  # Initial size, adjust as needed
        self.root.title("Coordinate App")
        self.root.resizable(width=False, height=False)

        # Configure column and row weights for centering
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.takeoff_landing_label = tk.Label(root, text="Takeoff/Landing:")
        self.takeoff_landing_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.latitude_label = tk.Label(root, text="Latitude:")
        self.latitude_label.grid(row=1, column=0, sticky="w")

        self.longitude_label = tk.Label(root, text="Longitude:")
        self.longitude_label.grid(row=2, column=0, sticky="w")

        self.latitude_entry = tk.Entry(root)
        self.latitude_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        self.longitude_entry = tk.Entry(root)
        self.longitude_entry.grid(row=2, column=1, columnspan=2, sticky="w")

        self.add_button = tk.Button(root, text="Add Coordinates", command=controller.add_coordinates)
        self.add_button.grid(row=3, column=1, columnspan=2, sticky="w")
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2)

        self.latitude_label2 = tk.Label(root, text="Latitude")
        self.latitude_label2.grid(row=5, column=0, sticky="w")

        self.longitude_label2 = tk.Label(root, text="Longitude:")
        self.longitude_label2.grid(row=6, column=0, sticky="w")

        self.latitude_entry2 = tk.Entry(root)
        self.latitude_entry2.grid(row=5, column=1, columnspan=2, sticky="w")

        self.longitude_entry2 = tk.Entry(root)
        self.longitude_entry2.grid(row=6, column=1, columnspan=2, sticky="w")

        self.generate_button = tk.Button(root, text="Generate Plan", command=controller.generate_plan)
        self.generate_button.grid(row=7, column=1, columnspan=2, sticky="w")

        # Expand all columns and rows
        for i in range(3):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)




class Controller:
    def __init__(self, root):
        self.planArr = []
        self.model = Model()
        self.view = View(root, self)

    def add_coordinates(self):
        additionalLat = self.view.latitude_entry2.get()
        additionalLong = self.view.longitude_entry2.get()

        if additionalLat and additionalLong:
            self.model.add_coordinate(additionalLat,additionalLong)
            self.view.result_label.config(text="Coordinates added successfully.")
        else:
            self.view.result_label.configure(text="Please enter both coordinates")
            
    def generate_plan(self):
        toLat = self.view.latitude_entry.get()
        toLong = self.view.longitude_entry.get()
        takeOffCoords = (toLat, toLong)
        self.planArr.append(takeOffCoords)
        self.planArr.extend(self.model.coordinates)
        self.planArr.append(takeOffCoords)
        self.view.result_label.configure(text="Plan generated!")
        print(self.planArr)
        return self.planArr

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()