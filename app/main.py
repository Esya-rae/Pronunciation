from fastapi import FastAPI, File, UploadFile
from fastapi.param_functions import Body
from fastapi.params import File
from pydantic import BaseModel
from random import randint
from  app.Word import Word
from app.Decode import To_phonemes
import app.Compare
import os

import requests
import shutil

app = FastAPI()

db = []

t_p = To_phonemes()

@app.get('/word')
def get_word():
    return db[randint(0, len(db))]

@app.post('/word')
def add_word(word: Word):
    db.append(word.dict())
    return db[-1]

@app.delete('/word/{word_id}')
def delete_word(word_id: int):
    db.pop(word_id - 1)
    return {}

@app.post('/audio')
def create_audio(word: str, file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    decoded_audio = ''.join(t_p.decode(file.filename).data)
    print(decoded_audio, word)
    os.remove(file.filename)
    return app.Compare.find_right_phonemes(decoded_audio, word)
