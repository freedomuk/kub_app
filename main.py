import json
from fastapi import FastAPI,Depends
from tasks import *
from models import User
from redis_client import redis_client
from sqlalchemy.orm import Session
from models import get_db,Base,engine
from prometheus_fastapi_instrumentator import Instrumentator
import os

app = FastAPI()
Instrumentator().instrument(app).expose(app)

items = []

@app.get('/write_data/{text_data}')
def write_data(text_data:str):
    with open('data.txt','a') as f:
        f.write(text_data)
    return f'Ok - {text_data}'

@app.get('/read_text')
def read_text():
    with open('data.txt','r') as f:
        res = f.read()
        return res

@app.get("/config")
def get_config():
    return {
        "app_name": os.getenv("APP_NAME"),
        "env": os.getenv("ENV"),
        "color": os.getenv("MY_COLOR"),
        "city": os.getenv("MY_CITY"),
        "message": os.getenv("MY_MESSAGE"),
        "password": os.getenv("MY_PASSWORD")
    }

@app.get("/")
def read_root():
    return {'Good':'a'}

@app.get("/a")
def read_root():
    return {'Good':'bb'}

@app.get("/b")
def read_root():
    return {'Good':'ccc'}

import time

@app.get("/get_info/{a}/{b}")
def get_info(a: int, b: int):

    cache_key = f"sum:{a}:{b}"

    cached = redis_client.get(cache_key)

    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")
    time.sleep(5)

    result = {"res": a + b}

    redis_client.setex(
        cache_key,
        60,
        json.dumps(result)
    )

    return result

@app.post('/create_item')
def create_item(item:dict):
    items.append(item)
    return item

@app.get('/get_items')
def get_items():
    return items


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.post("/users")
def create_user(name: str, db: Session = Depends(get_db)):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name} for u in users]


