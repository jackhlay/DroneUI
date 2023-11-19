from pymavlink import mavutil
import math
import tkinter as tk
import pygame
import transformations as tft

def get_distance_global(current_lat, current_lon, target_lat, target_lon):
    #return the distance between current position and target position in centimeters
    #does not account for the curvature of the earth

    delta_lat = target_lat - current_lat
    delta_lon = target_lon - current_lon

    if delta_lat <= 1 or delta_lon <= 1:
        return 0

    distance  = math.sqrt(delta_lat ** 2 + delta_lon ** 2) #formula for euclidean distance between 2 points
    return distance #mavlink GPS coords are represented in units of 10,000,000, so this line converts degrees to cm. 

def get_distance_local(curr_x, curr_y, curr_z, x, y, z):
    return math.sqrt((curr_x - x)**2 + (curr_y - y)**2 + (curr_z - z)**2)

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

#send local frame coordinates and have copter fly over that spot.
def send_waypoint_local(connection, x, y, alt):
    connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message
                    (10, connection.target_system, connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
                     int(0b010111111000), x, y, alt,
                      0, 0, 0, 0, 0, 0, 0, 0))

    while 1:
        msg = connection.recv_match(type = 'LOCAL_POSITION_NED', blocking = True)
        
        current_x = msg.x
        current_y = msg.y
        current_z = msg.z

        print("current x: %d" % current_x)

        distance = get_distance_local(current_x, current_y, current_z, x, y, alt)

        print("distance to target: %d" % distance)

        if(distance <= 3): #break when we are within 50 cm of target
            print("target waypoint reached")
            break


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

        print("distance to target: %d" % distance)

        if(distance <= 50): #break when we are within 50 cm of target
            print("target waypoint reached")
            break

def send_manual_control(connection, x, y, z, r):
    q = tft.quaternion_from_euler(x, y, r)
    
    # Send SET_ATTITUDE_TARGET message

    connection.mav.set_attitude_target_send(
        0,  # time_boot_ms
        connection.target_system,
        connection.target_component,
        0b00000000,  # Type mask
        q,  # Quaternion
        0, 0, 0,  # Body roll, pitch, yaw rate
        z # Thrust

    )

#parse through the array of coordinates generated by the MVC and fly to each point
def process_planArr(connection, planArr, alt):
    print("sending takeoff command")
    takeoff(connection, alt)
    for lat, lon in planArr:
        if (lat):
            print("Going to lat: %s lon: %s" % (lat, lon))
            send_waypoint_local(connection, float(lat) , float(lon) , alt)
    land(connection)


#Main code:

drone_connection = connect(14550) #udp connection to ardupilot

takeoff(drone_connection, 2)

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()

# Check for joystick count
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick detected")
    exit()

# Initialize the Joystick
joystick = pygame.joystick.Joystick(0)

joystick.init()

try:
    while True:
        pygame.event.pump()

        # Joystick axes
        left_joystick_x = int(joystick.get_axis(0) * 1000)  # Scale to -1000 to 1000
        left_joystick_y = int(joystick.get_axis(1) * 1000)
        right_joystick_x = int(joystick.get_axis(2) * 1000)
        right_joystick_y = int(joystick.get_axis(3) * 1000)

        # Clamp the values to ensure they are within the acceptable range
        left_joystick_x = max(-1000, min(1000, left_joystick_x))
        left_joystick_y = max(-1000, min(1000, left_joystick_y))
        right_joystick_x = max(-1000, min(1000, right_joystick_x))
        right_joystick_y = max(-1000, min(1000, right_joystick_y))

        # Convert throttle input from -1000 to 1000 range to 0 to 1000
        throttle = int((left_joystick_y + 1) * 500)  # Scale and shift to 0 to 1000
        throttle = max(0, min(1000, throttle))  # Clamp throttle

        # Send manual control commands
        send_manual_control(drone_connection, right_joystick_x, right_joystick_y, throttle, left_joystick_x)

except KeyboardInterrupt:
    print("Exiting...")
    land(drone_connection)
finally:
    pygame.quit()