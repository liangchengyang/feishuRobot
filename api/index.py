# coding:utf-8
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Response

app = FastAPI()


class Msg(BaseModel):
    code: int
    msg: str
    data: dict = {}


@app.get("/api")
def news():
    return Msg(code=1, msg="success")


if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8001)
