from fastapi import FastAPI, WebSocket
from typing import Dict

app = FastAPI()

# Store WebSocket connections by client ID
clients: Dict[str, WebSocket] = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # Get and log the client's IP address
    client_ip = websocket.client.host
    print(f"Client connected: {client_id}, IP: {client_ip}")

    await websocket.accept()
    clients[client_id] = websocket

    try:
        while True:
            # Relay signaling messages between peers without processing them
            data = await websocket.receive_text()
            for _, connection in clients.items():
                if connection != websocket:  # Forward to all other peers
                    await connection.send_text(data)
    except Exception as e:
        print(f"Connection with {client_id} closed: {e}")
    finally:
        del clients[client_id]
        print(f"Client disconnected: {client_id}, IP: {client_ip}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
