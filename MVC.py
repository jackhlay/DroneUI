import tkinter as tk

class Model:
    def __init__(self):
        self.coordinates = [] #Coordinate array

    def add_coordinate(self, latitude, longitude):
        self.coordinates.append((latitude, longitude))

    def generate_plan(self):
        print("Generating plan with coordinates:", self.coordinates)

class View: #ugly view monolith

    def __init__(self, root, controller):
        self.root = root
        self.root.geometry("360x480")  # Initial size, adjust as needed
        self.root.title("Coordinate App")
        self.root.resizable(width=False, height=False) #Only technically though

        self.takeoff_landing_label = tk.Label(root, text="Takeoff/Landing:") # takeoff/landing Label
        self.takeoff_landing_label.grid(row=0, column=0, columnspan=3, sticky="nsew")# " positioning

        self.latitude_label = tk.Label(root, text="Latitude:") # Instantiating Takeoff Latitiude Label
        self.latitude_label.grid(row=1, column=0, sticky="w")

        self.longitude_label = tk.Label(root, text="Longitude:") # Instantiating Takeoff Logitude Label
        self.longitude_label.grid(row=2, column=0, sticky="w")

        self.latitude_entry = tk.Entry(root) # Instantiating latitude text box
        self.latitude_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        self.longitude_entry = tk.Entry(root) # Instantiating latitude text box
        self.longitude_entry.grid(row=2, column=1, columnspan=2, sticky="w")

        self.add_button = tk.Button(root, text="Add Coordinates", command=controller.add_coordinates) # Intantiate button to add coordinates to plan
        self.add_button.grid(row=3, column=1, columnspan=2, sticky="w")
        self.result_label = tk.Label(root, text="") #Creating dynamic result label
        self.result_label.grid(row=4, column=0, columnspan=2)

        self.latitude_label2 = tk.Label(root, text="Latitude") #Insantiate Label for Additional Latitude
        self.latitude_label2.grid(row=5, column=0, sticky="w")

        self.longitude_label2 = tk.Label(root, text="Longitude:") # Instantiate Label for Additinal Longitude
        self.longitude_label2.grid(row=6, column=0, sticky="w")

        self.latitude_entry2 = tk.Entry(root) # Instantiate Label for Additinal latitude
        self.latitude_entry2.grid(row=5, column=1, columnspan=2, sticky="w")

        self.longitude_entry2 = tk.Entry(root) # Instantiate Label for Additinal Longitude
        self.longitude_entry2.grid(row=6, column=1, columnspan=2, sticky="w")

        self.generate_button = tk.Button(root, text="Fly", command=controller.generate_plan) # Instantiate Button to send commands
        self.generate_button.grid(row=7, column=1, columnspan=2, sticky="w")

        # Expand all columns and rows
        for i in range(3):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)




class Controller:
    def __init__(self, root):
        self.planArr = [] #In   
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
        toLat = self.view.latitude_entry.get() #get Takeoff / Landing lat
        toLong = self.view.longitude_entry.get() #get Takeoff / Landing long
        takeOffCoords = (toLat, toLong) #make coordinate pair
        self.planArr.append(takeOffCoords) #adding takeoff cap
        self.planArr.extend(self.model.coordinates) #Adding points to the plan array
        self.planArr.append(takeOffCoords) #addinf landing cap
        self.view.result_label.configure(text="Plan generated!")
        #print(self.planArr)
        self.view.root.destroy() #close the window
        return self.planArr
    


if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
