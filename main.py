from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Session, create_engine, Column, DateTime, Text, func
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

print("Iniciando aplicación...")

class Libro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ean: str = Field()
    link: str = Field(index=True)
    descripcion: str = Field(index=True, nullable=True)
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
    SQLModel.metadata.create_all(engine, checkfirst=True)

create_db_and_tables()


app = FastAPI()

############API
class LibroCreate(BaseModel):
    ean: str
    link: str
    descripcion: str | None = None
    marc21: str | None = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/libro")
def create_libro(libro: LibroCreate):
    new_libro = Libro(**libro.dict())
    print(new_libro.dict())
    with Session(engine) as session:
        session.add(new_libro)
        session.commit()
    return libro

@app.get("/libros/{ean}")
def get_libro_by_ean(ean: str):
    with Session(engine) as session:
        libro = session.query(Libro).filter(Libro.ean == ean).order_by(Libro.id.desc()).first()
        # libro = session.query(Libro).filter(Libro.ean == ean).first()

        if not libro:
            return {"error": "Libro no encontrado"}
        return libro