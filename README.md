# FastAPI Auth & CRUD Project

FastAPIを使用した、JWT認証とItem管理（CRUD）機能を持つバックエンドプロジェクトです。
セキュアな認証機能と、ユーザーごとのデータ管理機能を備えています。

## 主な機能

- **ユーザー認証**: 
  - **Argon2**: セキュアなパスワードハッシュ化アルゴリズムを採用
  - **JWT (JSON Web Token)**: ステートレスでスケーラブルな認証
- **アイテムCRUD**:
  - 認証済みユーザーによるアイテムの作成・取得・更新・削除
  - ユーザーごとのデータ分離（自分のアイテムのみ操作可能）
- **自動テスト**:
  - `pytest` を使用した包括的なテストスイート
  - テスト実行ごとにデータベースを自動的にリセット・初期化

## 🛠 技術スタック

| カテゴリ | 技術 |
| :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ORM / DB** | [SQLAlchemy](https://www.sqlalchemy.org/) (SQLite) |
| **認証 / セキュリティ** | [python-jose](https://github.com/mpdavis/python-jose), [passlib](https://passlib.readthedocs.io/) |
| **テスト** | [pytest](https://docs.pytest.org/), [httpx](https://www.python-httpx.org/) |

## セットアップ

### 1. 依存関係のインストール

プロジェクトルートで以下のコマンドを実行します。

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの実行

```bash
uvicorn myapp.main:app --reload
```

実行後、[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) にアクセスすることで、Swagger UIからインタラクティブにAPIを試すことができます。

## テストの実行

```bash
python -m pytest
```

### テスト構成の詳細
- **共通設定**: `myapp/tests/conf_test.py` にて、テスト用DBの作成や共通フィクスチャが定義されています。
- **データクリーンアップ**: 各テストが走る前にデータベースが初期化されるため、テスト間の副作用がありません。

## プロジェクト構成

```text
.
├── myapp/
│   ├── auth/           # JWT認証・パスワードハッシュ関連
│   ├── crud/           # データベース操作（CRUD）
│   ├── models/         # SQLAlchemyモデル
│   ├── schemas/        # Pydanticスキーマ
│   ├── service/        # ビジネスロジック
│   ├── tests/          # pytestテストコード
│   ├── main.py         # アプリケーション・エントリポイント
│   └── database.py     # データベース接続・セッション管理
├── pytest.ini          # pytest設定ファイル
└── requirements.txt    # 依存ライブラリ一覧
```

