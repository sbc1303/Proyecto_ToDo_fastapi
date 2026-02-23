from pydantic import BaseModel, Field, field_validator
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

# Estado como Enum para evitar strings libres como "hecho" o "terminado"
class Estado(str, Enum):
    Pendiente = "Pendiente"
    En_progreso = "En progreso"
    Completada = "Completada"


class TareaInput(BaseModel):
    titulo: str = Field(..., min_length=3)  # mínimo 3 caracteres
    descripcion: Optional[str] = None
    prioridad: Prioridad = Prioridad.Media
    etiquetas: List[EtiquetasOpcion] = []
    fecha_vencimiento: Optional[str] = None

    # Se comprueba que el Datatime tenga el formato: DD-MM-YYYY antes de guardar.
    @field_validator("fecha_vencimiento")
    @classmethod
    def validar_fecha(cls, v):
        if v is None:
            return v
        try:
            from datetime import datetime
            datetime.strptime(v, "%d-%m-%Y")
        except ValueError:
            raise ValueError("La fecha debe tener formato DD-MM-YYYY")
        return v

class Tarea(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str] = None
    prioridad: Prioridad
    etiquetas: List[EtiquetasOpcion] = []
    fecha_vencimiento: Optional[str] = None
    estado: Estado = Estado.Pendiente
    completada: bool = False # booleano para consultas rápidas sin comparar strings
    fecha_creacion: str
    fecha_actualizacion: Optional[str] = None
    fecha_eliminacion: Optional[str] = None
    esta_activa: bool = True # False cuando está en la papelera


# Modelo separado para el PATCH de estado, así no hay necesidad de mandar el objeto entero
class EstadoUpdate(BaseModel):
    nuevo_estado: Estado

# Modelo para editar solo título y descripción y que ambos sean opcionales
class TareaEdit(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3)
    descripcion: Optional[str] = None