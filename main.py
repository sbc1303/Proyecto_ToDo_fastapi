from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import Tarea, TareaInput, EstadoUpdate, Estado, TareaEdit
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


# Creación de tareas
@app.post("/tasks", status_code=201, response_model=Tarea, tags=["1. Tareas generales"], summary="Crear tarea")
def crear_tarea(tarea_in: TareaInput):
    lista = leer_db()
    # El id es el máximo actual + 1, así nunca se repite aunque se borren tareas
    nuevo_id = max([t["id"] for t in lista], default=0) + 1
    nueva_tarea = Tarea(
        id=nuevo_id,
        **tarea_in.model_dump(),
        fecha_creacion=obtener_hora()
    )
    lista.append(nueva_tarea.model_dump())
    guardar_db(lista)
    return nueva_tarea

@app.patch("/tasks/{id}", response_model=Tarea, tags=["1. Tareas generales"], summary="Editar tarea")
def editar_tarea(id: int, cambios: TareaEdit):
    lista = leer_db()
    for t in lista:
        if t["id"] == id and t.get("esta_activa"):
            if cambios.titulo is not None:
                t["titulo"] = cambios.titulo
            if cambios.descripcion is not None:
                t["descripcion"] = cambios.descripcion
            t["fecha_actualizacion"] = obtener_hora()
            guardar_db(lista)
            return t
    raise HTTPException(status_code=404, detail="No encontrada")


# Búsqueda
# Funciona como un buscador: se le intruduce unos valores y te devuelve la primera tarea que coincida con estos valores.
# Se han añadido otros parametros de busqueda que no se basen solo en el id (puede olvidarse), por lo que se puede buscar por título, prioridad o fechas.
@app.get("/tasks/busqueda", response_model=Tarea, tags=["2. Búsqueda"], summary="Buscador de tarea")
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


# Actualización del estado de las tareas
@app.patch("/tasks/{id}/estado", response_model=Tarea, tags=["3. Actualización del estado de la tarea"], summary="Actualizar estado de la tarea")
def actualizar_estado(id: int, body: EstadoUpdate):
    lista = leer_db()
    for t in lista:
        if t["id"] == id and t.get("esta_activa"):
            t["estado"] = body.nuevo_estado
            # El booleano completada lo actualizo aquí para no tener que comparar strings luego
            t["completada"] = body.nuevo_estado == Estado.Completada
            t["fecha_actualizacion"] = obtener_hora()
            guardar_db(lista)
            return t
    raise HTTPException(status_code=404, detail="No encontrada")


# Listado de tareas y papelera
# Con ver_papelera=true se puede ver las tareas eliminadas
# Con ordenar_por se puede ordenar por prioridad, fecha_creacion o fecha_vencimiento

@app.delete("/tasks/{id}", tags=["4. Eliminación de tareas y papelera"], summary="Eliminar tarea")
def eliminar_tarea(id: int):
    lista = leer_db()
    for t in lista:
        if t["id"] == id:
            # No se borra del JSON, solo se desactivca para no perder toda la información y poder restaurarla luego
            t["esta_activa"] = False
            t["fecha_eliminacion"] = obtener_hora()
            guardar_db(lista)
            return {"mensaje": "Eliminado"}
    raise HTTPException(status_code=404, detail="No encontrada")

@app.get("/tasks", response_model=list[Tarea], tags=["4. Eliminación de tareas y papelera"], summary="Búsqueda de tareas eliminadas")
def buscar_tareas(
    ver_papelera: bool = False,
    ordenar_por: Optional[str] = None
):
    lista = leer_db()
    resultado = [t for t in lista if t.get("esta_activa") == (not ver_papelera)]

    # Urgente primero, Baja al final
    orden_prioridad = {"Urgente": 0, "Alta": 1, "Media": 2, "Baja": 3}

    if ordenar_por == "prioridad":
        resultado.sort(key=lambda t: orden_prioridad.get(t.get("prioridad", "Baja"), 99))
    elif ordenar_por == "fecha_creacion":
        resultado.sort(key=lambda t: t.get("fecha_creacion", ""))
    elif ordenar_por == "fecha_vencimiento":
        # Las tareas sin fecha de vencimiento van al final
        resultado.sort(key=lambda t: t.get("fecha_vencimiento") or "9999-99-99")

    return resultado

# Busca la tarea que se encuentran incativas o en la papelera y se reactivan
@app.patch("/tasks/{id}/restaurar", response_model=Tarea, tags=["4. Eliminación de tareas y papelera"], summary="Restaurar tarea")
def restaurar_tarea(id: int):
    lista = leer_db()
    for t in lista:
        if t["id"] == id and not t.get("esta_activa"):
            t["esta_activa"] = True
            t["fecha_eliminacion"] = None
            t["fecha_actualizacion"] = obtener_hora()
            guardar_db(lista)
            return t
    raise HTTPException(status_code=404, detail="No encontrada o no está en la papelera")


# Panel de control 
@app.get("/dashboard", tags=["5. Panel de control"], summary="Estadísticas")
def estadisticas():
    activas = [t for t in leer_db() if t["esta_activa"]]
    return {
        "total": len(activas),
        "completadas": len([t for t in activas if t.get("completada")]),
        "pendientes": len([t for t in activas if t.get("estado") == "Pendiente"]),
        "en_progreso": len([t for t in activas if t.get("estado") == "En progreso"])
    }