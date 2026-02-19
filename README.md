# API REST - Gestor de Tareas

API para gestionar tareas desarrollada con FastAPI. Los datos se guardan en un archivo JSON local, sin base de datos.

El proyecto cubre los requisitos del enunciado y le he ido añadiendo cosas a medida que avanzaba y veía que tenían sentido: borrado lógico, búsqueda flexible por varios campos, un panel de estadísticas y un sistema de escritura segura del JSON para no perder datos si algo falla.

---

## Lo que he añadido respecto a los requisitos básicos

- **Backup automático al guardar**: antes de escribir en el JSON hago una copia. Además escribo en un archivo temporal y luego reemplazo el original, así si la app se cierra mal a mitad de una escritura el archivo no queda corrupto.
- **Borrado lógico con papelera**: al eliminar una tarea no la borro del JSON, la marco como inactiva. Con `?ver_papelera=true` en el GET puedes ver las tareas eliminadas.
- **Búsqueda flexible**: el endpoint de búsqueda acepta id, título, prioridad y fechas. Devuelve la primera tarea que coincida con cualquiera de los parámetros, sin necesidad de saber el id exacto.
- **Modelo de datos ampliado**: prioridad, etiquetas, y fechas de creación, actualización y eliminación.
- **Panel de control**: un endpoint extra con el total de tareas activas y cuántas están completadas.
- **Código separado en módulos**: `main.py`, `models.py` y `database.py` para que sea más fácil de leer y modificar.
- **Docker**: Dockerfile incluido para levantar la app en un contenedor.

---

## Estructura

```
proyecto_todo_fastapi/
├── main.py          # endpoints
├── models.py        # modelos Pydantic
├── database.py      # lectura y escritura del JSON
├── requirements.txt
├── Dockerfile
└── database.json    # se crea solo al añadir la primera tarea
```

---

## Instalación

**Local:**

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Docker:**

```bash
docker build -t gestor-tareas .
docker run -d -p 8000:8000 gestor-tareas
```

---

## Endpoints

| Método | Ruta                 | Descripción                                                 |
| ------ | -------------------- | ----------------------------------------------------------- |
| POST   | `/tasks`             | Crear tarea                                                 |
| GET    | `/tasks`             | Listar tareas activas (o papelera con `?ver_papelera=true`) |
| GET    | `/tasks/busqueda`    | Buscar por id, título, prioridad o fechas                   |
| PATCH  | `/tasks/{id}/estado` | Cambiar el estado de una tarea                              |
| DELETE | `/tasks/{id}`        | Mover a la papelera                                         |
| GET    | `/dashboard`         | Estadísticas                                                |

---

## Probar la API

Con la app corriendo, la documentación interactiva está en:

```
http://localhost:8000/docs
```

**Crear una tarea:**

```json
POST /tasks
{
  "titulo": "Estudiar para el examen",
  "prioridad": "Alta",
  "etiquetas": ["Estudio"],
  "fecha_vencimiento": "2025-03-01"
}
```

**Cambiar estado:**

```json
PATCH /tasks/1/estado
{
  "nuevo_estado": "Completada"
}
```
