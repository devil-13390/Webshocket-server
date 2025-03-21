import asyncio
import websockets

# Store active target connections {password: websocket}
active_targets = {}

async def handler(websocket, path):
    password = await websocket.recv()  # Receive Target's unique password
    active_targets[password] = websocket
    print(f"Target {password} connected.")

    try:
        async for message in websocket:
            print(f"Received from {password}: {message}")
    except:
        pass
    finally:
        del active_targets[password]  # Remove Target on disconnect
        print(f"Target {password} disconnected.")

async def get_active_targets(websocket):
    await websocket.send(",".join(active_targets.keys()))

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
