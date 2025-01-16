from fastapi import FastAPI, WebSocket
from typing import Dict
import json

app = FastAPI()

# Store WebSocket connections by client ID
clients: Dict[str, WebSocket] = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # Add "target" field to your signaling messages
            target_id = message.get("target")

            if target_id in clients:
                await clients[target_id].send_text(data)
            else:
                print(f"Target {target_id} not connected")
    except Exception as e:
        print(f"Connection with {client_id} closed: {e}")
    finally:
        del clients[client_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
