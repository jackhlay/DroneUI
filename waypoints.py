from pymavlink import mavutil
import math
import tkinter as tk
import MVC

def get_distance_global(current_lat, current_lon, target_lat, target_lon):
    #return the distance between current position and target position in centimeters
    #does not account for the curvature of the earth

    delta_lat = target_lat - current_lat
    delta_lon = target_lon - current_lon
    distance  = math.sqrt(delta_lat ** 2 + delta_lon ** 2) #formula for euclidean distance between 2 points
    return distance #mavlink GPS coords are represented in units of 10,000,000, so this line converts degrees to cm. 


def connect(port):
    print("Attempting to connect on port %d" % port)

    connection = mavutil.mavlink_connection('udpin:localhost:%d' % port) 

    connection.wait_heartbeat() #wait until we hear a heartbeat from the copter

    print("Connection success")
    print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))

    return connection 

def takeoff(connection, takeoff_alt):
    #arm throttle (copter has to be in guided mode)
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

#send local frame coordinates and have copter fly over that spot.
def send_waypoint_local(connection, x, y, alt):
    connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message
                    (10, connection.target_system, connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
                     int(0b010111111000), x, y, alt,
                      0, 0, 0, 0, 0, 0, 0, 0))

    while 1:
        msg = connection.recv_match(type = 'LOCAL_POS', blocking = True)
        print(msg)

#send global gps coordinates and altitude, and have copter fly over that spot. 
def send_waypoint_global(connection, lat, lon, alt):
    connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message
                    (10, connection.target_system, connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                     int(0b110111111000), int(lat), int(lon), alt, 0, 0, 0, 0, 0, 0, 0, 0))
    #loop until we reach target waypoint
    while 1:
        msg = connection.recv_match(type = 'GLOBAL_POSITION_INT', blocking = True)

        current_lat = msg.lat 
        current_lon = msg.lon

        distance = get_distance_global(current_lat, current_lon, lat, lon)

        print("Current distance %d" % distance)

        if(distance <= 50): #break when we are within 50 cm of target
            print("target waypoint reached")
            break

def process_planArr(connection, planArr, alt):
    print("sending takeoff command")
    takeoff(connection, alt)
    for lat, lon in planArr:
        print("Going to lat: %s lon: %s" % (lat, lon))
        send_waypoint_global(connection, float(lat) * 1e7, float(lon) *1e7, alt)
    land(connection)


#Main code:
root = tk.Tk()
app = MVC.Controller(root)
root.mainloop()
planArr = app.planArr

print("waypoints to visit:")
print(planArr)

drone_connection = connect(14551)

process_planArr(drone_connection, planArr, 10)