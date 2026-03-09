# Gestor de Tareas - API REST con FastAPI

Este proyecto consiste en el desarrollo de una **API REST con FastAPI** para gestionar una lista de tareas.  
Los datos se almacenan en un **archivo JSON local**, sin utilizar una base de datos.

Para el desarrollo del proyecto se plantearon inicialmente unos **endpoints básicos**, pero durante la implementación surgieron varias ideas que aportaban valor al proyecto, como por ejemplo:

- Borrado lógico
- Búsqueda avanzada por diferentes campos
- Organización de endpoints por categorías
- Sistema de logging
- Escritura segura del JSON con backup

---

# Tecnologías utilizadas

Para el desarrollo de este proyecto se han utilizado las siguientes tecnologías:

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- Docker

---

# Cómo ejecutar el proyecto

El proyecto puede ejecutarse **en local** o **mediante Docker**.

## Ejecutar en local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

La API estará disponible en:

```
http://localhost:8000
```

La documentación interactiva (Swagger):

```
http://localhost:8000/docs
```

## Interfaz Swagger

La API incluye documentación automática generada por FastAPI mediante Swagger, donde se pueden probar todos los endpoints directamente desde el navegador.

![Swagger](docs/swagger.png)

---

## Ejecutar con Docker

```bash
docker build -t gestor-tareas .
docker run -d -p 8000:8000 gestor-tareas
```

---

# Endpoints disponibles

La API cuenta con los siguientes endpoints agrupados por categorías.

| Método | Ruta | Descripción |
|------|------|------|
| POST | /tasks | Crear una tarea nueva |
| GET | /tasks | Listar todas las tareas activas |
| GET | /tasks?ver_papelera=true | Ver tareas eliminadas |
| GET | /tasks?ordenar_por=prioridad | Ordenar por prioridad, fecha_creacion o fecha_vencimiento |
| GET | /tasks/busqueda | Buscar por id, título, prioridad o fechas |
| PATCH | /tasks/{id} | Editar título y/o descripción |
| PATCH | /tasks/{id}/estado | Cambiar el estado de una tarea |
| DELETE | /tasks/{id} | Mover una tarea a la papelera |
| PATCH | /tasks/{id}/restaurar | Restaurar una tarea desde la papelera |
| DELETE | /tasks/papelera/vaciar | Vaciar la papelera definitivamente |
| GET | /dashboard | Ver estadísticas generales |

---

# Estructura del proyecto

El código está dividido en varios archivos para facilitar su mantenimiento y ampliación.

```
Proyecto_ToDo_fastapi/
├── main.py          # Contiene todos los endpoints organizados por categorías
├── models.py        # Modelos Pydantic, Enum y validaciones
├── database.py      # Lectura y escritura del JSON + sistema de backup
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── database.json    # Se genera automáticamente al crear la primera tarea
```

---

# Funciones añadidas para aportar valor al proyecto

Durante el desarrollo se añadieron varias funcionalidades adicionales:

### Borrado lógico

Las tareas eliminadas no se borran del JSON, se marcan como inactivas. Esto permite restaurarlas posteriormente.

### Búsqueda flexible

Permite buscar tareas no solo por ID, sino también por título, prioridad o fechas.

### Ordenación del listado

Las tareas pueden ordenarse por:

- prioridad
- fecha de creación
- fecha de vencimiento

### Validación de fechas

La fecha de vencimiento solo acepta el formato:

```
DD-MM-YYYY
```

Si el formato no es correcto, la API devuelve un error.

### Estado como Enum

Los estados posibles están definidos como Enum para evitar valores incorrectos:

- Pendiente
- En proceso
- Completada

### Panel de estadísticas

El endpoint `/dashboard` muestra:

- total de tareas
- tareas completadas
- tareas pendientes
- tareas en proceso

### Logging

Cada vez que se lee o escribe el archivo JSON se registra un mensaje en consola.  
Si el archivo está corrupto, el sistema intenta restaurarlo desde un backup.

### Escritura segura del JSON

Antes de sobrescribir el JSON se genera una copia de seguridad y se utiliza un archivo temporal para evitar corrupción del archivo.

---

# Ejemplos de uso

Las peticiones se pueden probar desde:

```
http://localhost:8000/docs
```

o mediante herramientas como **Postman**.

---

## Crear una tarea

```
POST /tasks
```

```json
{
  "titulo": "Estudiar para el examen",
  "prioridad": "Alta",
  "etiquetas": ["Estudio"],
  "fecha_vencimiento": "01-03-2025"
}
```

---

## Cambiar el estado de una tarea

```
PATCH /tasks/1/estado
```

```json
{
  "nuevo_estado": "Completada"
}
```

---

## Buscar una tarea por título

```
GET /tasks/busqueda?titulo=examen
```

---

## Ordenar tareas por prioridad

```
GET /tasks?ordenar_por=prioridad
```

---

## Eliminar una tarea (borrado lógico)

```
DELETE /tasks/1
```

---

## Ver tareas eliminadas

```
GET /tasks?ver_papelera=true
```

---

## Restaurar una tarea

```
PATCH /tasks/1/restaurar
```

---

## Eliminar definitivamente las tareas de la papelera

```
DELETE /tasks/papelera/vaciar
```
