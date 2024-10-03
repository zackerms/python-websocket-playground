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