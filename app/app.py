import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Mapped, mapped_column, Session

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


reg = registry()
engine = create_engine(
    'postgresql+psycopg://app_user:app_password@localhost:5433/app_db'
)

@reg.mapped_as_dataclass
class Pessoa:
    __tablename__ = 'pessoas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(default='Taconi')



@asynccontextmanager
async def lifespan(app):
    logger.info('Iniciando app')
    reg.metadata.create_all(engine)
    yield
    logger.info('Finalizando app')
    reg.metadata.drop_all(engine)


app = FastAPI(lifespan=lifespan)


@app.get('/check')
def check():
    logger.info('App OK')
    return {'status': 'ok'}


class PessoaSchemaIn(BaseModel):
    nome: str

class PessoaSchemaOut(BaseModel):
    nome: str


def create_user(pessoa: PessoaSchemaIn):
    dump = pessoa.model_dump()

    p = Pessoa(**dump)

    logger.info('Criando Pessoa', extra=dump)

    with Session(engine) as session:
        session.add(p)
        session.commit()
        session.refresh(p)

        return p