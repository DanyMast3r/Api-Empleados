from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from pydantic import BaseModel

# Conexión a la base de datos MySQL con SQLAlchemy
SQLALCHEMY_DATABASE_URL = "mysql://root:@localhost/api"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definición de la clase base para las tablas
Base = declarative_base()

# Definición del modelo de datos para el empleado utilizando SQLAlchemy
class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    edad = Column(String, index=True)
    cargo = Column(String, index=True)
    salario = Column(String, index=True)

# Definición del modelo Pydantic para el empleado
class EmpleadoPydantic(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: str
    cargo: str
    salario: str

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Funciones de acceso a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_empleado(db, empleado_id: int):
    empleado = db.query(Empleado).filter(Empleado.id == empleado_id).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado

def create_empleado(db, empleado: EmpleadoPydantic):
    db_empleado = Empleado(**empleado.dict())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

def update_empleado(db, empleado_id: int, empleado: EmpleadoPydantic):
    db_empleado = get_empleado(db, empleado_id)
    for key, value in empleado.dict().items():
        setattr(db_empleado, key, value)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

def delete_empleado(db, empleado_id: int):
    db_empleado = get_empleado(db, empleado_id)
    db.delete(db_empleado)
    db.commit()
    return {"mensaje": "Empleado eliminado exitosamente"}

# Rutas
@app.post("/empleados/", response_model=EmpleadoPydantic)
def crear_empleado(empleado: EmpleadoPydantic, db: Session = Depends(get_db)):
    return create_empleado(db, empleado)

@app.get("/empleados/{empleado_id}", response_model=EmpleadoPydantic)
def obtener_empleado(empleado_id: int, db: Session = Depends(get_db)):
    return get_empleado(db, empleado_id)

@app.put("/empleados/{empleado_id}", response_model=EmpleadoPydantic)
def actualizar_empleado(empleado_id: int, empleado: EmpleadoPydantic, db: Session = Depends(get_db)):
    return update_empleado(db, empleado_id, empleado)

@app.delete("/empleados/{empleado_id}")
def eliminar_empleado(empleado_id: int, db: Session = Depends(get_db)):
    return delete_empleado(db, empleado_id)