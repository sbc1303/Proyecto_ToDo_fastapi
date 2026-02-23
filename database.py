import json
import os
import shutil
import logging
from datetime import datetime

DB_FILE = "database.json"
BACKUP_FILE = "database_backup.json"

# Configuro el logger para ver en consola cuándo se lee o escribe la base de datos
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def leer_db():
    if not os.path.exists(DB_FILE):
        logger.info("No existe el archivo de base de datos, se devuelve lista vacía")
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
            logger.info(f"Base de datos leída correctamente ({len(datos)} tareas)")
            return datos
    except (json.JSONDecodeError, IOError):
        # Si el JSON está corrupto intento tirar del backup
        logger.warning("El JSON está corrupto, intentando recuperar desde backup")
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


def guardar_db(datos):
    # Hago una copia antes de tocar nada, por si algo falla
    if os.path.exists(DB_FILE):
        shutil.copy(DB_FILE, BACKUP_FILE)

    # Escribo en un temporal y luego reemplazo el original
    # así si se corta a mitad no dejo el JSON corrupto
    temp_file = f"temp_{DB_FILE}"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    os.replace(temp_file, DB_FILE)
    logger.info(f"Base de datos guardada correctamente ({len(datos)} tareas)")


def limpiar_papelera():
    # Borra definitivamente del JSON todas las tareas inactivas (en la papelera)
    datos = leer_db()
    activas = [t for t in datos if t.get("esta_activa")]
    eliminadas = len(datos) - len(activas)
    guardar_db(activas)
    logger.info(f"Papelera limpiada: {eliminadas} tareas eliminadas definitivamente")
    return eliminadas


def obtener_hora():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
