import asyncio
from mavsdk import System

async def run():
    drone=System()
    print("connecting to px4........")
    await drone.connect(system_address="udpin://0.0.0.0:14540")
    print('waiting for the drone to connect')

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"drone connected")
            break
    print("arming...")
    await drone.action.arm()
    print("armed..")

    
    print("taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(10)


    print("Getting altitude at home location")
    home= await anext(drone.telemetry.home())

    absolute_altitude=home.absolute_altitude_m
    absolute_latitude=home.latitude_deg
    absolute_longitude=home.longitude_deg

    flying_alt=absolute_altitude+5.0
    print(f"Flight altitude is: {flying_alt}")

    print("going to target 1 location...")
    await drone.action.goto_location(absolute_latitude+10 * 1e-5,absolute_longitude,flying_alt,0)
    await asyncio.sleep(10)

    print("going to target 2 location...")
    await drone.action.goto_location(absolute_latitude+10 * 1e-5,absolute_longitude +10 * 1e-5,flying_alt,0)
    await asyncio.sleep(10)

    print("going to target 3 location...")
    await drone.action.goto_location(absolute_latitude,absolute_longitude +10 * 1e-5,flying_alt,0)
    await asyncio.sleep(10)

    print("going to target 4 location...")
    await drone.action.goto_location(absolute_latitude,absolute_longitude,flying_alt,0)
    await asyncio.sleep(10)
    
    print('landing...')
    await drone.action.land()
    await asyncio.sleep(10)

    print('drone landed!!!')
asyncio.run(run())


