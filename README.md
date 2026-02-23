# Gestor de Tareas - API REST con FastAPI

Este proyecto se basa en el desarrollo de una API REST con FastAPI para gestionar una lista de tareas donde los datos se almacenan en un archivo JSON local, sin usar una base de datos.

Para este proyecto se han pedido unos requisitos (Endpoints) básicos pero durante la creación de estos, fueron surgiendo ideas o mejoras que tenían sentido y aportaban valor al proyecto como han sido:

- Borrado lógico
- Búsqueda avanzada donde no solo se puede realizar la búsqueda en base a la ID, sino por más campos.
- Organización de los endpoints por categorías
- Logging

---

## Tecnologías utilizadas

Para el desarrollo de este proyecto se han utilizado las siguientes tecnologías:

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- Docker

---

## Cómo ejecutar el proyecto

Este proyecto se puede ejecutar tanto en local como en Docker, por lo que para acceder en cada una de las opciones se seguirán los siguientes pasos:

- En local:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

- Con Docker:

```bash
docker build -t gestor-tareas .
docker run -d -p 8000:8000 gestor-tareas
```

---

## Endpoints disponibles

La API cuenta con los siguientes endpoints agrupados por categorías. La documentación interactiva (Swagger) está disponible en `http://localhost:8000/docs`. Donde se pueden probar directamente todas las peticiones:

| Método | Ruta                           | Descripción                                               |
| ------ | ------------------------------ | --------------------------------------------------------- |
| POST   | `/tasks`                       | Crear una tarea nueva                                     |
| GET    | `/tasks`                       | Listar todas las tareas activas                           |
| GET    | `/tasks?ver_papelera=true`     | Ver tareas eliminadas                                     |
| GET    | `/tasks?ordenar_por=prioridad` | Ordenar por prioridad, fecha_creacion o fecha_vencimiento |
| GET    | `/tasks/busqueda`              | Buscar por id, título, prioridad o fechas                 |
| PATCH  | `/tasks/{id}`                  | Editar título y/o descripción                             |
| PATCH  | `/tasks/{id}/estado`           | Cambiar el estado de una tarea                            |
| DELETE | `/tasks/{id}`                  | Mover una tarea a la papelera                             |
| PATCH  | `/tasks/{id}/restaurar`        | Restaurar una tarea desde la papelera                     |
| DELETE | `/tasks/papelera/vaciar`       | Vaciar la papelera definitivamente                        |
| GET    | `/dashboard`                   | Ver estadísticas generales                                |

---

## Estructura del proyecto

El código está separado en tres archivos principales para que sea más fácil la lectura, modificación o ampliación. Cada archivo tiene una función determinada:

```
Proyecto_ToDo_fastapi/
├── main.py          # Aquí están todos los endpoints, separados por categorías
├── models.py        # Los modelos Pydantic, con los Enum y las validaciones
├── database.py      # Todo lo relacionado con leer y escribir el JSON, incluido el backup
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── database.json    # Se genera automáticamente al crear la primera tarea
```

---

## Funciones añadidas para dar valor al proyecto

Como se ha comentado en la primera parte, durante la creación de la API, han ido surgiendo apartados que considero que dan un valor añadido al trabajo. Como son:

- **Borrado lógico**: las tareas eliminadas no se borran del JSON, se marcan como inactivas. Así se pueden restaurar si hace falta.
- **Búsqueda flexible**: no hace falta saber el id exacto, puedes buscar por título, prioridad o fechas.
- **Ordenación del listado**: por prioridad, fecha de creación o fecha de vencimiento.
- **Validación de fechas**: la fecha de vencimiento solo acepta el formato DD-MM-YYYY, si no lo cumple da error.
- **Estado como Enum**: evita que se pueda guardar cualquier string como estado.
- **Panel de estadísticas**: muestra el total de tareas, cuántas están completadas, pendientes y en progreso.
- **Logging**: cada vez que se lee o escribe el JSON aparece un mensaje en consola. También avisa si el archivo está corrupto y tira del backup.
- **Escritura segura del JSON**: antes de escribir se hace una copia de seguridad. Además se usa un archivo temporal para que si la app se cierra a mitad de una escritura el JSON no quede corrupto.

---

## Ejemplos de uso

A continuación se muestran algunos ejemplos de las peticiones más comunes. Para poder comprobarlo se puede usar Swagger en `http://localhost:8000/docs` o cualquier herramienta (en este caso también se ha utilizado Postman):

**Crear una tarea:**

```json
POST /tasks
{
  "titulo": "Estudiar para el examen",
  "prioridad": "Alta",
  "etiquetas": ["Estudio"],
  "fecha_vencimiento": "01-03-2025"
}
```

**Cambiar el estado:**

```json
PATCH /tasks/1/estado
{
  "nuevo_estado": "Completada"
}
```

**Buscar una tarea por título:**

```
GET /tasks/busqueda?titulo=examen
```

**Revisar las tareas ordenadas por prioridad:**

```
GET /tasks?ordenar_por=prioridad
```

**Eliminar una tarea (se mueve a la papelera, no se borra definitivamente):**

```
DELETE /tasks/1
```

**Ver las tareas eliminadas y si se desea, restaurar la tarea:**

```
GET /tasks?ver_papelera=true
```

```json
PATCH /tasks/1/restaurar
```

**Si se desea eliminar la tarea definitivamente:**

```
DELETE /tasks/papelera/vaciar
```
