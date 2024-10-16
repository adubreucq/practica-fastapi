from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Column, DateTime, Text, func
from contextlib import asynccontextmanager
from datetime import datetime

app = FastAPI()

print("Iniciando aplicación...")

class Libro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ean: str = Field()
    link: str = Field(index=True)
    descripcion: str = Field(index=True)
    marc21: str = Field(sa_column=Column(Text(), nullable=True))
    create_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

engine = create_engine('mysql+pymysql://root:root@localhost:3306/prueba-libros', echo=True)

try:
    engine.connect()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")

def create_db_and_tables():
    print("Creando tablas en la base de datos...")
    SQLModel.metadata.create_all(engine, checkfirst=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Conectando a la base de datos...")
    create_db_and_tables()  # Crear tablas al inicio
    yield
    # Aquí puedes poner lógica de apagado si lo necesitas
create_db_and_tables()

app = FastAPI(lifespan=lifespan)
