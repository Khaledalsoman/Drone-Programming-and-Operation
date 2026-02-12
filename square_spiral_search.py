import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan


async def run():
    drone = System()
    print("Connecting to drone...")
    await drone.connect(system_address="udp://:14540")

    start_lat_step = int(input("Start point latitude steps (e.g., 5): "))
    start_lon_step = int(input("Start point longitude steps (e.g., 5): "))

    print("Arming drone...")
    await drone.action.arm()
    await asyncio.sleep(5)

    print("Taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    home = await anext(drone.telemetry.home())

    lat = home.latitude_deg
    lon = home.longitude_deg
    alt = 5.0

    print(f"Flight altitude is: {alt}")

    mission_items = []

    for i in range(50):
        size = i * 10e-5
        

        mission_items.extend([
            # Top Right
            MissionItem(lat + size, lon + size, alt, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'),
                        float('nan'), float('nan'),
                        float('nan'), MissionItem.VehicleAction.NONE),

            # Top Left
            MissionItem(lat + size, lon - size, alt, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'),
                        float('nan'), float('nan'),
                        float('nan'), MissionItem.VehicleAction.NONE),

            # Bottom Left
            MissionItem(lat - size, lon - size, alt, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'),
                        float('nan'), float('nan'),
                        float('nan'), MissionItem.VehicleAction.NONE),

            # Bottom Right
            MissionItem(lat - size, lon + size, alt, 5.0, True,
                        float('nan'), float('nan'), MissionItem.CameraAction.NONE,
                        float('nan'), float('nan'),
                        float('nan'), float('nan'),
                        float('nan'), MissionItem.VehicleAction.NONE),
        ])
        
        mission_plan = MissionPlan(mission_items)

        print("Uploading mission...")
        await drone.mission.upload_mission(mission_plan)
        await asyncio.sleep(2)

        print("Starting mission...")
        await drone.mission.start_mission()
        await asyncio.sleep(2)



asyncio.run(run())
