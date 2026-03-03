from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# -----------------------------------------------------------------------------------------
# sqlalchemy → library jo Python ko database se connect karne deti hai.
# create_engine → function jo database connection banata hai.

# 🔹 sessionmaker
# Database se baat karne ke liye session banata hai.
# Har request me ek naya DB session create karte hain.


# 🔹 declarative_base
# Ye base class banata hai jisse hum apne models (tables) define karte hain.
# Jaise class User(Base):
# ---------------------------------------------------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# isme DATABASE_URL basically ye batata h ki konsa database h and kaha located h and kis type ka h 

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
# ye tables defination ke liye base class h 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# yield db ka basically ye kaam hota h ki - 
# pehle db ko route function ko de do and thn route ka kaam hone do .
# jab rote ka kaam khatam ho jaye tab neeche ka code chalado 


# finally: db.close()
# Ye ensure karta hai:

# 👉 Chahe request successful ho
# 👉 Chahe error aaye

# Session band ho hi jayega
# Agar close nahi karoge:

# Connections accumulate honge
# Server slow hoga
# Crash bhi ho sakta hai