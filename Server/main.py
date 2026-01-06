from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from services.processing import process_pdf, chat_with_pdf

app = FastAPI()

load_dotenv()

origins_env = os.getenv("ALLOWED_ORIGINS", "")
allow_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"success": "ChatWithPDF Server Running..."}


@app.post("/upload-pdf")
def upload_pdf(file: UploadFile):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    process_pdf(file.filename)
    return {"message": "PDF uploaded and processed"}


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(req: ChatRequest):
    answer = chat_with_pdf(req.question)
    return {"answer": answer}
