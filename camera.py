from djitellopy import Tello
import cv2

drone=Tello()
drone.connect()
drone.streamon()

while True:
    frame=drone.get_frame_read().frame
    cv2.imshow('drone camera',frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

frame=drone.get_frame_read().frame
cv2.imwrite('images\images.jpg',frame)
print('image saved')

drone.streamoff()