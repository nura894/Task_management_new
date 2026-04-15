from fastapi import FastAPI
from database.db_postgres import engine
from models import Base
from router import auth, delete_account, task_manage
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Task Management")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(delete_account.router)
app.include_router(task_manage.router)



@app.get("/")
def home():
    return {"message": "FastAPI is working "}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)