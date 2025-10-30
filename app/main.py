from fastapi import FastAPI
from app.routes import auth, events, swap
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(swap.router)
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the Slot Swapper API"}
