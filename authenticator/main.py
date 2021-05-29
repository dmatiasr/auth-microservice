from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
from schemas import AuthDetails


app = FastAPI()


auth_handler = AuthHandler()
users = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any( x.get('username') == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail="Username already exist")
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        "username": auth_details.username,
        "password": hashed_password
    })

    return 200


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x.get("username") == auth_details.username:
            user = x 
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.get("password"))):
        raise HTTPException(status_code=401, detail="Invalid username nor password")
    token = auth_handler.encode_token(user.get("username"))
    
    return {"token": token}


@app.get('/free')
def free():
    return {"Hello": "World"}


@app.get('/private')
def private(username=Depends(auth_handler.auth_wrapper)):
    return {"name": username}