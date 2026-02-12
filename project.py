import asyncio
import math
import numpy as np
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

async def main():
    drone = System()
    print("Connecting to drone...")
    await drone.connect(system_address="udp://:14540")
    
    home = await anext(drone.telemetry.home())
    absolute_latitude = home.latitude_deg
    absolute_longitude = home.longitude_deg

    target_height_m = eval(input("Enter the flying height (m): "))  # meters
    await drone.action.set_takeoff_altitude(target_height_m)

    print("Arming drone...")
    await drone.action.arm()
    await asyncio.sleep(5)
    
    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    print(f"Home Longtidue: {absolute_longitude} ")
    print(f"Home Latitude: {absolute_latitude} ")

    print("--------------------------------------------")
    print("What is the expected location (to start with)?\n")
    target_longitude = eval(input("Enter the longitude (deg): "))
    target_latitude = eval(input("Enter the latitude (deg): "))
    print("--------------------------------------------")

    # camera_FOV_deg = eval(input("Enter the FOV of the camera (deg): "))

    # area_size_m = eval(input("Enter the size of the area to be covered (m): "))

    # overlap_percentage = eval(input("Enter the desired overlap percentage (0-100): "))

    # vision_width_m = 2 * target_height_m * math.tan(math.radians(camera_FOV_deg / 2))

    # print(f"Vision width covered by the camera is: {vision_width_m} (m)")

    mission_items = []
    move_horz = False
    move_ver = True
    moved_dis = 0
    counter = 0

    horz_change = 10 * 1e-5
    ver_change = 10 * 1e-5

    accumulated_horz_change = horz_change
    accumulated_ver_change = ver_change

    mission_items.append(MissionItem(target_latitude, target_longitude, target_height_m, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'), float('nan'), float('nan'),
                        float('nan'),MissionItem.VehicleAction.NONE))

    while True:

        if move_horz == True:
            mission_items.append(MissionItem(target_latitude, target_longitude + accumulated_horz_change, target_height_m, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'), float('nan'), float('nan'),
                        float('nan'),MissionItem.VehicleAction.NONE))
            move_horz = False
            move_ver = True
            target_longitude = target_longitude + accumulated_horz_change
            accumulated_horz_change = -1 * (accumulated_horz_change + np.sign(accumulated_horz_change) * horz_change)

        elif move_ver == True:
            mission_items.append(MissionItem(target_latitude + accumulated_ver_change, target_longitude, target_height_m, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'), float('nan'), float('nan'),
                        float('nan'),MissionItem.VehicleAction.NONE))
            move_horz = True
            move_ver = False
            target_latitude = target_latitude + accumulated_ver_change
            accumulated_ver_change = -1 * (accumulated_ver_change + np.sign(accumulated_ver_change) * ver_change)

        if counter == 10:
            break

        counter += 1
        # if moved_dis == area_size_m or counter == 10:
        #     break

        # moved_dis += vision_width_m / 2

    mission_plan = MissionPlan(mission_items)

    print("Uploading mission...")
    await drone.mission.upload_mission(mission_plan)
    await asyncio.sleep(2)

    print("Starting mission...")
    await drone.mission.start_mission()
    await asyncio.sleep(2)

    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")
        if mission_progress.current == mission_progress.total:
            print("-- Mission completed!")
            break

    print("Going to home...")
    await drone.action.goto_location(absolute_latitude, absolute_longitude, float('nan'), float('nan'))
    await asyncio.sleep(10)

    print("Landing...")
    await drone.action.land()
    await asyncio.sleep(10)

asyncio.run(main())
            



    # print("Landing...")
    # await drone.action.land()
    # await asyncio.sleep(10)

    # print("Disarming drone...")
    # await drone.action.disarm()

# asyncio.run(main())