from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///events.db'

#creation de l'engine et du session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base pour les modeles
Base = declarative_base()


#fonction pour obtenir une session du db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() #liberer les ressources