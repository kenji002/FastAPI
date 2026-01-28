# 事前準備
```bash
# 1.仮想環境作成
python -m venv venv

# 2.仮想環境の起動
.\venv\Scripts\activate

# 3.依存関係のインストール
pip install -r requirements.txt

# 4.データベースの初期化
python app\database.py

# 5.開発用サーバーの起動
uvicorn app.main:app --reload

```
# 追加機能のセットアップ

## Pydantic v2 対応
```bash
# FastAPIを最新に更新
pip install -U fastapi
# バージョン確認(fastapi/pydantic)
pip show fastapi
pip show pydantic
```

## 認証（JWT）
```bash
# 必要ライブラリをインストール
pip install python-jose passlib[bcrypt]
pip install argon2_cffi
```

## MySQL / PostgreSQL 切替
```bash
# 必要ライブラリをインストール
pip install sqlalchemy[mysql]
pip install sqlalchemy[postgresql]
```

## pytest でテスト追加
```bash
# 必要ライブラリをインストール
pip install pytest
```
