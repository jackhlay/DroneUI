# Spot On Automated Drone Surveying System

This project implements a drone navigation system using Python. It allows users to input GPS coordinates, generates a flight plan, and controls a drone to fly over these coordinates.

## Modules

- `mavutil` from `pymavlink` for handling MAVlink communication.
- `math`
- `tkinter` GUI package
- `pytest` for testing 
- `TkinterMapView` from `tkintermapview` for embedded map in GUI
- `Image`, `ImageTk` from `PIL` for image processing of GUI icons
- `threading` for running simultaneous threads of execution

## Project Structure

### Communication Class

Responsible for all the MAVLink communication with the drone, including sending commands and receiving information.

- `get_distance_global`: Calculates the Euclidean distance between two GPS points.
- `get_current_lat` and `get_current_lon`: Fetches the current latitude and longitude from the drone.
- `connect`: Establishes a connection to the drone.
- `takeoff`: Commands the drone to take off to a specified altitude.
- `land`: Commands the drone to land.
- `send_waypoint_global`: Sends a waypoint to the drone and waits until it reaches the location.
- `get_takeoff_lat` and `get_takeoff_lon`: Gets the latitude and longitude of the takeoff location.
- `process_planArr`: Processes an array of coordinates and commands the drone to fly to each point.
- `isInRange`: Checks if a target location is within a specified range from the takeoff point.

### SingletonRoot Class

A singleton class that extends `tk.Tk` for creating a single instance of the main application window.

### Model Class

Holds data related to GPS coordinates and notifies observers when changes occur.

- `add_coordinate`: Adds a new GPS coordinate.
- `register_observer` and `notify_observers`: Observer pattern implementation for MVC architecture.
- `generate_plan`: Generates a list of coordinates with the current coordinates.

### View Class

Manages the GUI for the application.

- Implements GUI elements.
- Functions to update the map view and coordinate list.
- Integrates with `TkinterMapView` for embedded map.

### Controller Class

Acts as an intermediary between the View and Model, handling user inputs and updating the view.

- `add_coordinates`: Adds coordinates to the model.
- `generate_plan`: returns a sequence of coordinates from the model's coordinates.
- `fly_button_pressed`: Initiates the drone operation sequence.
- `start_drone_operations`: Starts a new thread for drone operations to run while the GUI updates with the drone's location. 

### Main Execution

- Initializes the `SingletonRoot` and `Controller` classes.
- Starts the Tkinter main loop.

## Usage

- Run the script to start the application.
- Enter an address in the address bar to center the map view on the desired location.
- Right click on the locations where property markers will be placed, select 'add coordinates' from the drop down.
- Click 'Fly' to start the drone operation based on the provided coordinates.
- The map within the GUI window will update with the drone's current location in relation to each waypoint

