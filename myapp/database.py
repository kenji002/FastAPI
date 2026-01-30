from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

def get_db():
    """
    データベースセッションの依存性注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    with engine.connect() as conn:
        print("データベースに正常に接続しました")
except Exception as e:
    print(f"データベース接続エラー: {e}")