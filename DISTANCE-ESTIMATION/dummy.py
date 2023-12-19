from djitellopy import Tello
import time


tello = Tello()

tello.connect()
tello.takeoff()

tello.go_xyz_speed(30, 0, 0, 11)
time.sleep(2)

tello.go_xyz_speed(0, 30, 0, 11)
time.sleep(2)

tello.go_xyz_speed(0, 0, 20, 11)
time.sleep(2)

tello.land()

