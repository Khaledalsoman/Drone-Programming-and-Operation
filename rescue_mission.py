import asyncio
import random
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

async def run():
    start_lat_step = int(input("Start point latitude steps (e.g., 5): "))
    start_lon_step = int(input("Start point longitude steps (e.g., 5): "))

    # Simple settings
    moves = int(input("How many moves? (e.g., 6): "))

    drone = System()
    print("connecting to px4........")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("waiting for the drone to connect")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("drone connected")
            break

    print("arming...")
    await drone.action.arm()
    print("taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(8)

    print("Getting home location")
    home = await anext(drone.telemetry.home())

    lat = home.latitude_deg
    lon = home.longitude_deg
    alt = home.absolute_altitude_m + 5.0

    print("Going to mission start point...")
    lat = lat + start_lat_step * 1e-5
    lon = lon + start_lon_step * 1e-5
    await drone.action.goto_location(lat, lon, alt, 0)
    await asyncio.sleep(8)

    found = False
    for i in range(moves):
        
        r_lat = random.randint(-10, 10) * 1e-5
        r_lon = random.randint(-10, 10) * 1e-5

        lat = lat + r_lat
        lon = lon + r_lon

        print(f"Move {i+1}/{moves}: going to another location...")
        await drone.action.goto_location(lat, lon, alt, 0)
        await asyncio.sleep(6)

        # random decision: found or not
        if random.choice([True, False]):
            print("Missing person FOUND (simulation)!")
            found = True
            break
        else:
            print("Not found (simulation). Continue...")

    print("Returning home...")
    await drone.action.goto_location(home.latitude_deg, home.longitude_deg, alt, 0)
    await asyncio.sleep(8)

    print("landing...")
    await drone.action.land()
    await asyncio.sleep(10)

    if found:
        print("Mission result: FOUND ")
    else:
        print("Mission result: NOT FOUND ")

asyncio.run(run())
