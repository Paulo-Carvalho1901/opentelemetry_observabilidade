import logging 
from fastapi import FastAPI

logger = logging.getLogger()

app = FastAPI()


@app.get('/check')
def check():
    return {'status': 'Ok'}
