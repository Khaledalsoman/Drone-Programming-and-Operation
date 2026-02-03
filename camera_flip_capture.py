from djitellopy import Tello
import cv2

drone=Tello()
drone.connect()
drone.streamon()

drone.takeoff()


drone.move_forward(50)
drone.flip_back()

while True:
    frame=drone.get_frame_read().frame
    cv2.imshow('drone camera',frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
frame=drone.get_frame_read().frame
cv2.imwrite('camera flip record\images.jpg',frame)
print('image saved')

drone.streamoff()