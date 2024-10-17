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
```
```sh
uvicorn main:app
```