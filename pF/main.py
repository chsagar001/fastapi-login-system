from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pF.database import SessionLocal, engine
from pF.models import Base, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def serve_login_page():
    with open("pF/login.html", "r") as f:
        return f.read()

@app.post("/login")
def login(username: str, password: str):
    db = SessionLocal()
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    return JSONResponse(content={"message": "Login saved successfully"})

@app.get("/api", response_class=JSONResponse)
def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [{"username": user.username, "password": user.password} for user in users]