from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

# Inicializamos la base de datos SQLite
DATABASE_URL = "sqlite:///./asistencia.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Creamos la API
app = FastAPI()

# Middleware de CORS (permitir conexión desde frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos modelos de BD
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(Date, default=date.today())
    usuario = relationship("Usuario")

Base.metadata.create_all(bind=engine)

# Modelos de request/response
class UsuarioCreate(BaseModel):
    nombre: str

class AsistenciaCreate(BaseModel):
    usuario_id: int

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    class Config:
        orm_mode = True

class AsistenciaOut(BaseModel):
    id: int
    usuario: UsuarioOut
    fecha: date
    class Config:
        orm_mode = True

# Endpoints

@app.post("/usuarios", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    nuevo_usuario = Usuario(nombre=usuario.nombre)
    db.add(nuevo_usuario)
    try:
        db.commit()
        db.refresh(nuevo_usuario)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    finally:
        db.close()
    return nuevo_usuario

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    db.close()
    return {"mensaje": "Usuario eliminado"}

@app.get("/usuarios", response_model=List[UsuarioOut])
def listar_usuarios():
    db = SessionLocal()
    usuarios = db.query(Usuario).all()
    db.close()
    return usuarios

@app.post("/asistencia", response_model=AsistenciaOut)
def pasar_lista(asistencia: AsistenciaCreate):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == asistencia.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    nueva_asistencia = Asistencia(usuario_id=usuario.id)
    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)
    db.close()
    return nueva_asistencia

@app.get("/asistencia", response_model=List[AsistenciaOut])
def listar_asistencias():
    db = SessionLocal()
    asistencias = db.query(Asistencia).all()
    db.close()
    return asistencias

@app.get("/")
def raiz():
    return {"mensaje": "¡API de asistencia activa y funcionando!"}
