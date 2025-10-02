import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from sqlalchemy.orm import registry, Mapped, mapped_column

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


reg = registry()


@reg.mapped_as_dataclass
class Pessoa:
    __tablename__ = 'pessoas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(default='Davi')


@asynccontextmanager 
async def lifespan(app):
    logger.info('Iniciando app.')
    yield
    logger.info('Finalizando app.')

app = FastAPI(lifespan=lifespan)


@app.get('/check')
def check():
    logger.info('App OK')
    return {'status': 'Ok'}
