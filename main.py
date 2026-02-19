from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import Tarea, TareaInput, EstadoUpdate
from database import leer_db, guardar_db, obtener_hora

# Ordeno las etiquetas para que el Swagger quede más limpio
orden_etiquetas = [
    {"name": "1. Tareas generales"},
    {"name": "2. Búsqueda"},
    {"name": "3. Actualización del estado de la tarea"},
    {"name": "4. Eliminación de tareas y papelera"},
    {"name": "5. Panel de control"}
]

app = FastAPI(title="Gestor de Tareas", openapi_tags=orden_etiquetas)


# 1. TAREAS GENERALES
@app.post("/tasks", status_code=201, response_model=Tarea, tags=["1. Tareas generales"])
def crear_tarea(tarea_in: TareaInput):
    lista = leer_db()
    nuevo_id = max([t["id"] for t in lista], default=0) + 1
    nueva_tarea = Tarea(
        id=nuevo_id,
        **tarea_in.model_dump(),
        fecha_creacion=obtener_hora()
    )
    lista.append(nueva_tarea.model_dump())
    guardar_db(lista)
    return nueva_tarea


# 2. BÚSQUEDA
# Funciona como un buscador: le pasas lo que sabes y te devuelve la primera tarea que coincida.
# No hace falta saber el id exacto, puedes buscar por título, prioridad o fechas.
@app.get("/tasks/busqueda", response_model=Tarea, tags=["2. Búsqueda"])
def obtener_una_tarea(
    id: Optional[int] = None,
    titulo: Optional[str] = None,
    prioridad: Optional[str] = None,
    fecha_creacion: Optional[str] = None,
    fecha_vencimiento: Optional[str] = None
):
    for t in leer_db():
        if t.get("esta_activa"):
            if id is not None and t.get("id") == id:
                return t
            if titulo is not None and titulo.lower() in t.get("titulo", "").lower():
                return t
            if prioridad is not None and t.get("prioridad") == prioridad:
                return t
            if fecha_creacion is not None and t.get("fecha_creacion") == fecha_creacion:
                return t
            if fecha_vencimiento is not None and t.get("fecha_vencimiento") == fecha_vencimiento:
                return t

    raise HTTPException(status_code=404, detail="No encontrada")


# 3. ACTUALIZACIÓN DE ESTADO
@app.patch("/tasks/{id}/estado", response_model=Tarea, tags=["3. Actualización del estado de la tarea"])
def actualizar_estado(id: int, body: EstadoUpdate):
    lista = leer_db()
    for t in lista:
        if t["id"] == id and t.get("esta_activa"):
            t["estado"] = body.nuevo_estado
            # Si ponen "completada" o "terminada" marco el booleano también
            t["completada"] = body.nuevo_estado.lower() in ["completada", "terminada"]
            t["fecha_actualizacion"] = obtener_hora()
            guardar_db(lista)
            return t
    raise HTTPException(status_code=404, detail="No encontrada")


# 4. LISTADO Y PAPELERA
# Con ver_papelera=true puedes ver las tareas eliminadas
@app.get("/tasks", response_model=list[Tarea], tags=["4. Eliminación de tareas y papelera"])
def buscar_tareas(ver_papelera: bool = False):
    lista = leer_db()
    return [t for t in lista if t.get("esta_activa") == (not ver_papelera)]

@app.delete("/tasks/{id}", tags=["4. Eliminación de tareas y papelera"])
def eliminar_tarea(id: int):
    lista = leer_db()
    for t in lista:
        if t["id"] == id:
            t["esta_activa"] = False  # no borro del JSON, solo la desactivo
            t["fecha_eliminacion"] = obtener_hora()
            guardar_db(lista)
            return {"mensaje": "Eliminado"}
    raise HTTPException(status_code=404, detail="No encontrada")


# 5. PANEL DE CONTROL
@app.get("/dashboard", tags=["5. Panel de control"])
def estadisticas():
    activas = [t for t in leer_db() if t["esta_activa"]]
    return {
        "total": len(activas),
        "completadas": len([t for t in activas if t.get("completada")])
    }
