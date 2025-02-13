import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import notes_router

app = FastAPI()
notes = []
todos = []
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router, prefix="/notes")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)

