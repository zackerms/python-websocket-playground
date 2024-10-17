## 環境構築

### バックエンド
```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### フロントエンド
```sh
cd frontend
python -m http.server 3000
```

### アクセスポイント

| 種類 | URL |
| --- | --- |
| バックエンド | http://localhost:8000 |
| フロントエンド | http://localhost:3000 |


### ベンチマーク
```sh
python3 benchmark.py --n 100

# 詳細な設定
# --url: 接続先のURL
# --n: コネクション数
# --duration: 1コネクションあたりの接続時間
# --delay: コネクションを行う間隔
python3 benchmark.py \
    --url "ws://localhost:8000/ws/benchmark" \
    --n 1000 \
    --duration 100 \
    --delay 0.1
```
```sh
uvicorn main:app
```