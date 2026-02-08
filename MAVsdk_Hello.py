import asyncio
from mavsdk import System

async def run():
    drone=System()
    print("connecting to px4........")

    await drone.connect(System_addres="udp://:14540")
    print('drone connected')

    asyncio.run(run())