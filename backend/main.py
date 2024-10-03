from typing import List
from logging import getLogger
from fastapi import FastAPI, WebSocketDisconnect
from fastapi import FastAPI, WebSocket

app = FastAPI()
logger = getLogger(__name__)

@app.get("/")
def read_root():
    return {"Hello": "World"}

counter = 0
connections_counter: List[WebSocket] = []
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
    global connections_counter

    # 新しい接続を待機
    await websocket.accept()
    print("Accept new connection")

    # 接続されたクライアントを登録する
    connections_counter.append(websocket)

    # 現在のカウンターの値を送信
    await websocket.send_json({"counter": counter})

    try:
        while True:
            # クライアントからデータを受信
            data = await websocket.receive_json()
            counter += data["value"]
            print(f"Receive data: {data}")  

            # 接続された全クライアントにデータを送信
            for connection in connections_counter:
                await connection.send_json({"counter": counter})
    except WebSocketDisconnect:
        # クライアントが切断された場合、接続を削除する
        print("Disconnect")
        connections_counter.remove(websocket)
        # await websocket.close()

counter_a = 0
counter_b = 0
connections_mashing: List[WebSocket] = []
@app.websocket("/ws/mashing")
async def websocket_mashing(websocket: WebSocket):
    """
    Request:
    {
        "player": "a"
    }

    Response:
    {
        "a": 1,
        "b": 1,
    }
    """
    global counter_a
    global counter_b
    global connections_mashing

    # 新しい接続を待機
    await websocket.accept()
    print("Accept new connection")

    # 接続されたクライアントを登録する
    connections_mashing.append(websocket)

    # 現在のカウンターの値を送信
    await websocket.send_json({"a": counter_a, "b": counter_b})

    try:
        while True:
            # クライアントからデータを受信
            data = await websocket.receive_json()
            if data["action"] == "reset":
                counter_a = 0
                counter_b = 0
            elif data["player"] == "a":
                counter_a += 1
            elif data["player"] == "b":
                counter_b += 1
            print(f"Receive data: {data}")  

            # 接続された全クライアントにデータを送信
            for connection in connections_mashing:
                await connection.send_json({"a": counter_a, "b": counter_b})
    except WebSocketDisconnect:
        # クライアントが切断された場合、接続を削除する
        print("Disconnect")
        connections_mashing.remove(websocket)
        # await websocket.close()