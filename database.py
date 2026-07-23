from sqlalchemy import Column , create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL = "sqlite:///./test.db"

engine = create_engine(
    DB_URL,
    connect_args={
        "check_same_thread":False
    }
)


session = sessionmaker(
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()