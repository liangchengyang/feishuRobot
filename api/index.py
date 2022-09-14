# coding:utf-8
import logging
from typing import Any
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Form
app = FastAPI()

logger = logging.getLogger(__name__)


class CheckMsg(BaseModel):
    challenge: str = ""


class RobotMsg(BaseModel):
    code: int = 1


class RobotView(BaseModel):
    challenge: str = ""
    token: str = ""
    type: str = ""
    encrypt: str = ""
    source: str = ""


@app.post("/api")
def robot(robot_view: RobotView):
    logger.info(robot_view)
    print(robot_view)
    if robot_view.challenge:
        return CheckMsg(challenge=robot_view.challenge)
    return RobotMsg()


if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8001)
