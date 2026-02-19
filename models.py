from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class Prioridad(str, Enum):
    Urgente = "Urgente"
    Alta = "Alta"
    Media = "Media"
    Baja = "Baja"


class EtiquetasOpcion(str, Enum):
    TRABAJO = "Trabajo"
    CASA = "Casa"
    ESTUDIO = "Estudio"
    OTROS = "Otros"


class Estado(str, Enum):
    Pendiente = "Pendiente"
    En_progreso = "En progreso"
    Completada = "Completada"


class TareaInput(BaseModel):
    titulo: str = Field(..., min_length=3)
    descripcion: Optional[str] = None
    prioridad: Prioridad = Prioridad.Media
    etiquetas: List[EtiquetasOpcion] = []
    fecha_vencimiento: Optional[str] = None


class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    prioridad: Prioridad
    etiquetas: List[EtiquetasOpcion] = []
    fecha_vencimiento: Optional[str] = None
    estado: Estado = Estado.Pendiente      
    completada: bool = False
    fecha_creacion: str
    fecha_actualizacion: Optional[str] = None
    fecha_eliminacion: Optional[str] = None
    esta_activa: bool = True


class EstadoUpdate(BaseModel):
    nuevo_estado: Estado                   