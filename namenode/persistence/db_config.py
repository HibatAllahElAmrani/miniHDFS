from sqlalchemy import create_engine
from persistence.db_models import Base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///./namenode.db")

SessionLocal = sessionmaker(autocommit=False, 
autoflush=False, 
bind=engine)

Base.metadata.create_all(bind=engine)