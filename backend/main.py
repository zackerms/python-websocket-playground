from typing import List
from logging import getLogger
from fastapi import FastAPI, WebSocketDisconnect
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = getLogger(__name__)

counter = 0
connections: List[WebSocket] = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/ws/counter")
async def websocket_count(websocket: WebSocket):
    """
    Request:
    {
        "value": 1
    }

    Response:
    {
        "counter": 1
    }
    """
    global counter
    global connections

    # 新しい接続を待機
    await websocket.accept()
    print("Accept new connection")

    # 接続されたクライアントを登録する
    connections.append(websocket)

    # 現在のカウンターの値を送信
    await websocket.send_json({"counter": counter})

    try:
        while True:
            # クライアントからデータを受信
            data = await websocket.receive_json()
            counter += data["value"]
            print(f"Receive data: {data}")  

            # 接続された全クライアントにデータを送信
            for connection in connections:
                await connection.send_json({"counter": counter})
    except WebSocketDisconnect:
        # クライアントが切断された場合、接続を削除する
        print("Disconnect")
        connections.remove(websocket)
        # await websocket.close()