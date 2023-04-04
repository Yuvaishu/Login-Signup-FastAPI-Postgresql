from fastapi import FastAPI, Request
import asyncpg
import uvicorn
from fastapi import FastAPI,Depends,status,Response,HTTPException
from fastapi.responses import HTMLResponse
# from database import engine,SessionLocal
# import schemas,models,database,hashing,jwstoken
from sqlalchemy.orm import Session
# from hashing import Hash
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def index():
    with open("index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/signup")
async def signup(request: Request):
    form = await request.form()
    name = form["username"]
    password = form["password"]
    conn = await asyncpg.connect(user="postgres", password="queenpanda", database="matic", host="localhost")
    await conn.execute("INSERT INTO users (name, password) VALUES ($1, $2)", name, password)
    await conn.close()
    # return {"message": "Sign up successful"}
    response = RedirectResponse("details.html")
    return response

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    name = form["username"]
    password = form["password"]
    conn = await asyncpg.connect(user="postgres", password="queenpanda", database="matic", host="localhost")
    result = await conn.fetchrow("SELECT * FROM users WHERE name=$1 AND password=$2", name, password)
    await conn.close()
    if result:
        # return {"message": "Login successful"}
        response = RedirectResponse("details.html")
        return response
    else:
        return {"message": "Invalid username or password"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
