from fastapi import FastAPI
from app.routes import auth, events, swap
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://127.0.0.1:5500", 
    "http://localhost:5500",  
    "https://slot-swapper.onrender.com",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],       
)


app.include_router(auth.router)
app.include_router(events.router)
app.include_router(swap.router)
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the Slot Swapper API"}
