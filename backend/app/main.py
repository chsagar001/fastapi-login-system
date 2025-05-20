from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal, engine
from app.models import Base, User
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Path to the login.html relative to this file
login_html_path = Path(__file__).parent.parent.parent / "frontend" / "login.html"

@app.get("/login", response_class=HTMLResponse)
def get_login_form():
    return login_html_path.read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
def serve_welcome():
    return "<h2>Welcome to FastAPI Login System</h2>"

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    return JSONResponse(content={"message": "Login saved successfully"})

@app.get("/api")
def show_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [{"username": user.username, "password": user.password} for user in users]