from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL: str = os.getenv("DB_URL")  # type: ignore

engine = create_engine(DATABASE_URL)

sesslocal = sessionmaker(bind=engine)

Base = declarative_base()