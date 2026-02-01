from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings



engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_size=5,         # Pool de conexiones
    max_overflow=10      # Conexiones extra permitidas
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()