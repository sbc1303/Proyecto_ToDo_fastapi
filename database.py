import json
import os
import shutil
from datetime import datetime

DB_FILE = "database.json"
BACKUP_FILE = "database_backup.json"


def leer_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Si el JSON está corrupto intento tirar del backup
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


def obtener_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")