from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

'''
from typing import List

from fastapi import Request, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


class Item(BaseModel):
    prefered_topics: List[str]
    representation_vector: List[float]
    seen_cards: List[int]
    language: str


class Response(BaseModel):
    question: str
    text: str
    source: str
    provided_by: str
    vector: List[float]
    language: str
 #   image: FileResponse

app = FastAPI()

existing_test = [{
    "question": "What?1",
    "text": "This1",
    "source": "https://github.com/1perday",
    "provided_by": "None",
    "vector": [0.1,0.2,0.3],
    "language": "en"
}, {
    "question": "What?2",
    "text": "This2",
    "source": "https://github.com/1perday",
    "provided_by": "abc",
    "vector": [0.4,0.5,0.6],
    "language": "en"
}]

 
@app.get("/", response_model=List[Response])
async def get_body(request: Item):
    return existing_test
'''
