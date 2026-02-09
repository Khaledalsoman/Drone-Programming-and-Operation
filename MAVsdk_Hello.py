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
    print("aremed..")

    
    print("taking off...")
    await drone.action.takeoff()
    await asyncio.sleep(10)

    print('landing...')
    await drone.action.land()
    print('drone landed!!!')
asyncio.run(run())


