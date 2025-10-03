import logging
from dataclasses import asdict
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Mapped, mapped_column, Session

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


class PessoaSchemaIn(BaseModel):
    nome: str

class PessoaSchemaOut(BaseModel):
    nome: str


@app.post('/create', response_model=PessoaSchemaOut)
def create(pessoa: PessoaSchemaIn):
    dump = pessoa.model_dump()
    p = Pessoa(**dump)
    
    logger.info('Criando pessoa', extra=dump)

    with Session(engine) as session:
        session.add(p)
        session.commit()
        session.refresh(p)

    return p