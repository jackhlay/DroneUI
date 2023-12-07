from pymavlink import mavutil
import math
import tkinter as tk
import MVC
import pytest
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import threading
import time

class Communication:

    target_lat = None
    target_lon = None

    def get_distance_global(current_lat, current_lon, t_lat, t_lon):
        #return the distance between current position and target position in centimeters
        #does not account for the curvature of the earth

        delta_lat = t_lat - current_lat
        delta_lon = t_lon - current_lon
        distance  = math.sqrt(delta_lat ** 2 + delta_lon ** 2) #formula for euclidean distance between 2 points
        return distance 
    
    def get_current_lat(connection):
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        return msg.lat
    
    def get_current_lon(connection):
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        return msg.lon

    def get_current_distance(connection, lat, lon):
        msg = connection.recv_match(type = 'GLOBAL_POSITION_INT', blocking = True)

        current_lat = msg.lat 
        current_lon = msg.lon

        distance = Communication.get_distance_global(current_lat, current_lon, lat, lon)

        return distance

    def connect(port):
        print("Attempting to connect on port %d" % port)

        connection = mavutil.mavlink_connection('udpin:0.0.0.0:%d' % port) 

        connection.wait_heartbeat() #wait until we hear a heartbeat from the copter

        print("Connection success")
        print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))

        return connection 

    def takeoff(connection, takeoff_alt):
        #set copter to guided mode
        connection.mav.set_mode_send(connection.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4) 

        #arm throttle
        connection.mav.command_long_send(connection.target_system, connection.target_component, 
                                 mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

        msg = connection.recv_match(type = 'COMMAND_ACK', blocking = True)
        print(msg) #"result: 0" if it executed without error. If you get result: 4, you probably need to set the copter to guided mode.

        #send takeoff command to target altitude.
        connection.mav.command_long_send(connection.target_system, connection.target_component, 
                                 mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, takeoff_alt)

        msg = connection.recv_match(type = 'COMMAND_ACK', blocking = True)
        print(msg)

        #loop until copter reaches takeoff altitude
        while 1:
            # Wait for the next LOCAL_POSITION_NED message
            msg = connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    
            # Check if altitude is within a threshold of the target altitude
            if abs(msg.z * -1 - takeoff_alt) < 1.0:
                print("Reached target altitude")
                break

    def land(connection): 
        connection.mav.command_long_send(connection.target_system, connection.target_component, 
                                mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)

    #send global gps coordinates and altitude, and have copter fly over that spot. 
    def send_waypoint_global(connection, lat, lon, alt):
        connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message
                    (10, connection.target_system, connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                     int(0b110111111000), int(lat), int(lon), alt, 0, 0, 0, 0, 0, 0, 0, 0))
        #loop until we reach target waypoint
        i = 0
        while 1:
            i += 1
            
            distance = Communication.get_current_distance(connection, lat, lon)

            #print("Current distance %d" % distance)

            if(distance <= 25): #break when we are within 25 cm of target
                print("target waypoint reached")
                break

    def get_takeoff_lat(connection):
        msg = connection.recv_match(type = 'GLOBAL_POSITION_INT', blocking = True)
        return msg.lat
        
    def get_takeoff_lon(connection):
        msg = connection.recv_match(type = 'GLOBAL_POSITION_INT', blocking = True)
        return msg.lon


    #parse through the array of coordinates generated by the MVC and fly to each point
    def process_planArr(connection, planArr, alt):
        print("sending takeoff command")
        Communication.takeoff(connection, alt)
        for lat, lon in planArr:
            print("Going to lat: %s lon: %s" % (lat, lon))
            Communication.target_lat = lat
            Communication.target_lon = lon
            Communication.send_waypoint_global(connection, float(lat) *1e7, float(lon) *1e7, alt)

    def isInRange(takeoff_lat, takeoff_lon, target_lat, target_lon):
        if (Communication.get_distance_global(takeoff_lat, takeoff_lon, target_lat, target_lon) > 40000):
            print("Coordinate entered is out of range")
            return False
        else:
            return True

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
            self.title("Plan Generator")
            self.resizable(width=True, height=True)

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

        self.drone_png = Image.open("images/6735608.png")
        self.drone_icon = ImageTk.PhotoImage(self.drone_png.resize((20, 20), Image.ANTIALIAS))

        self.icon_png = Image.open("images/icon.png")
        self.map_icon = ImageTk.PhotoImage(self.icon_png.resize((40, 40), Image.ANTIALIAS))


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
        self.generate_button.grid(row=6, column=0, columnspan=2, sticky="nesw")

        self.distance_label = tk.Label(root, text="Distance: N/A")
        self.distance_label.grid(row=7, column=0, columnspan=2, sticky="w")

        self.next_button = tk.Button(root, text="next waypoint", command=controller.next_button_pressed)
        self.next_button.grid(row=7, column=1, columnspan=2, sticky="w")

        self.map_view = TkinterMapView(root, width=360, height=250, corner_radius=3)
        self.map_view.grid(row=11, columnspan=5, sticky="nesw")
        self.map_view.set_zoom(0)

        def add_coords(coords):
            print("Added coords:", coords)
            self.vList.insert(tk.END, coords)
            self.controller.add_coordinates(coords[0], coords[1])
            new_marker = self.map_view.set_marker(coords[0], coords[1], icon=self.map_icon)
    

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

    def update_map(self, connection):
        
        lat = Communication.get_current_lat(connection)
        lon = Communication.get_current_lon(connection)

        if hasattr(self, 'drone_marker'):
            self.drone_marker.delete()

        self.drone_marker = self.map_view.set_marker(lat/1e7, lon/1e7, icon=self.drone_icon)

        self.root.after(1000, lambda: self.update_map(connection))

    def update_distance_label(self, distance):
        self.distance_label.config(text="distance: " + str(distance))
        self.root.after(1000, self.check_update_distance)  # Schedule to check for distance update

    def check_update_distance(self):
        if self.controller.update_needed:
            self.update_distance_label(self.controller.current_distance)

            
        

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
        print("waypoints to visit:")
        print(self.planArr)  

        drone_connection = Communication.connect(14550)
        self.view.update_map(drone_connection)

        drone_thread = threading.Thread(target=self.start_drone_operations, args=(drone_connection,))
        drone_thread.start()

        self.root.destroy()



    def start_drone_operations(self, connection):
        takeoff_lat = Communication.get_takeoff_lat(connection)
        takeoff_lon = Communication.get_takeoff_lon(connection)

        Communication.process_planArr(connection, self.planArr, 10)

        Communication.send_waypoint_global(connection, takeoff_lat, takeoff_lon, 10)
        Communication.land(connection)

if __name__ == "__main__":
    root = SingletonRoot()
    app = Controller(root)
    root.mainloop()
    root.quit()
