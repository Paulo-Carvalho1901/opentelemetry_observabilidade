import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Mapped, mapped_column

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


reg = registry()
engine = create_engine('sqlite:///:memory:')

@reg.mapped_as_dataclass
class Pessoa:
    __tablename__ = 'pessoas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(default='Davi')


@asynccontextmanager 
async def lifespan(app):
    logger.info('Iniciando app.')
    reg.metadata.create_all(engine)
    yield
    reg.metadata.drop_all(engine)
    logger.info('Finalizando app.')


app = FastAPI(lifespan=lifespan)


@app.get('/check')
def check():
    logger.info('App OK')
    return {'status': 'Ok'}


@app.post('/create')
def create():
    logger.info('Criando pessoa', extra={})