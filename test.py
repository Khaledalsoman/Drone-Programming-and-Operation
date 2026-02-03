from djitellopy import Tello
drone1 = Tello()
drone1.connect()
drone1.takeoff()

drone1.rotate_clockwise(35)
drone1.move_forward(50)

drone1.rotate_clockwise(90)
drone1.move_forward(50)

drone1.rotate_clockwise(35)
drone1.move_forward(50)

drone1.land()