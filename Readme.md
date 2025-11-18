Aquí lo tienes: **un README.md serio, completo, profesional y pensado para concurso**, explicando:

- Estructura del proyecto
- Cómo funciona FastAPI
- Qué son los routers
- Qué son los schemas
- Qué son los models
- Qué es SQLAlchemy y cómo se relaciona
- Cómo usar Pydantic v2 y pydantic-settings
- Cómo añadir tablas, claves foráneas, relaciones 1-N y N-N
- Cómo extender el proyecto de forma correcta
- Cómo ejecutar con Docker

Todo en un tono formal, limpio y totalmente listo para presentar.

---

# 📘 FastAPI Base Starter – Proyecto Template (Docker + SQLite + SQLAlchemy + Pydantic v2)

Este proyecto es una **plantilla base profesional** para construir APIs con **FastAPI**, organizada siguiendo prácticas recomendadas, totalmente dockerizada, y con **SQLite** como base de datos por defecto (fácilmente reemplazable por PostgreSQL o MySQL).

Incluye:

- 🚀 **FastAPI** (routers bien estructurados)
- 🗂 **Estructura modular**: `models`, `schemas`, `services`, `routers`, `core`
- 🧱 **SQLAlchemy ORM** con soporte para relaciones
- 🧪 **Pydantic v2 + pydantic-settings**
- 🐋 **Docker + Docker Compose**
- 💾 **SQLite en volumen persistente `/data`**
- 🔧 Código limpio, mantenible y listo para ampliarse

---

# 🏗️ Estructura del Proyecto

```
.
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── data/             # Aquí vive app.db (SQLite persistente)
└── app/
    ├── main.py       # Punto de entrada FastAPI
    ├── db.py         # Conexión DB y SessionLocal
    ├── core/
    │   └── config.py # Settings con pydantic-settings
    ├── models/
    │   └── user.py   # Modelos SQLAlchemy
    ├── schemas/
    │   └── user.py   # Schemas Pydantic (entrada/salida)
    ├── services/
    │   └── user_service.py # Lógica de negocio
    └── routers/
        └── users.py  # Endpoints REST
```

Esta arquitectura separa responsabilidades:

| Carpeta      | Rol                                                               |
| ------------ | ----------------------------------------------------------------- |
| **models**   | Define tablas SQLAlchemy (cómo se almacenan los datos).           |
| **schemas**  | Define validaciones y estructuras de entrada/salida con Pydantic. |
| **services** | Contiene la lógica (crear, consultar, actualizar…).               |
| **routers**  | Contiene endpoints FastAPI que llaman a los services.             |
| **core**     | Configuración global, como settings y variables de entorno.       |

---

# ⚙️ Instalación y ejecución

## Requisitos

- Docker
- Docker Compose

## Levantar el proyecto

```bash
docker compose up --build
```

La API estará disponible en:

📄 Documentación automática:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

📄 OpenAPI JSON:
**[http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)**

---

# 🧩 Explicación de FastAPI

FastAPI trabaja principalmente con:

### ✔ **Routers**

Son los "controladores" o "endpoints".
Ejemplo (`app/routers/users.py`):

```python
@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user_in)
```

Aquí:

- Recibe datos validados por Pydantic (`UserCreate`)
- Obtiene una sesión de DB (`Depends(get_db)`)
- Llama al service para ejecutar la lógica

---

# 🧱 Explicación de SQLAlchemy ORM

SQLAlchemy es un ORM que convierte clases Python en tablas SQL.

Ejemplo (`app/models/user.py`):

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    nombre = Column(String)
```

Esto crea internamente la tabla:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE,
    nombre VARCHAR
);
```

### Cómo crear relaciones

---

## 🔗 1–N (uno a muchos)

Ejemplo: un usuario → muchos posts.

### Modelo User:

```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

    posts = relationship("Post", back_populates="autor")
```

### Modelo Post:

```python
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    autor_id = Column(Integer, ForeignKey("users.id"))

    autor = relationship("User", back_populates="posts")
```

---

## 🔗 N–N (muchos a muchos)

Necesita una tabla intermedia:

```python
asociacion = Table(
    "usuarios_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)
```

Modelos:

```python
class User(Base):
    roles = relationship("Role", secondary=asociacion, back_populates="users")

class Role(Base):
    users = relationship("User", secondary=asociacion, back_populates="roles")
```

---

# 🧪 Explicación de Pydantic v2

Pydantic valida datos y controla qué se expone en la API.

Ejemplo (`schemas/user.py`):

```python
class UserCreate(BaseModel):
    email: EmailStr
    nombre: str | None = None
```

### Validación automática

Si envías:

```json
{ "email": "noesunemail" }
```

llega un error 422 automáticamente.

### `UserRead` controla lo que se devuelve:

```python
class UserRead(BaseModel):
    id: int
    email: EmailStr
    nombre: str | None
    class Config:
        from_attributes = True
```

---

# 🧠 Servicios (Business Logic)

Los services separan lógica de los endpoints:

```python
def create_user(db: Session, user_in: UserCreate):
    user = User(email=user_in.email, nombre=user_in.nombre)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

Ventajas:

- Los routers quedan limpios
- Ideal para tests
- Se puede reutilizar la lógica en otros módulos

---

# ⚙️ Configuración con pydantic-settings

Archivo: `app/core/config.py`

```python
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:////data/app.db"
```

Permite cargar valores desde `.env` automáticamente.

Ejemplo `.env`:

```
DATABASE_URL=sqlite:////data/app.db
DEBUG=true
```

Uso:

```python
from app.core.config import settings

print(settings.DATABASE_URL)
```

---

# 🧠 Cómo añadir una nueva tabla

1. Crear modelo en `app/models/mi_modelo.py`
2. Crear schema en `app/schemas/mi_modelo.py`
3. Crear service en `app/services/mi_modelo_service.py`
4. Crear router en `app/routers/mi_modelo.py`
5. Registrar el router en `main.py`:

```python
app.include_router(mi_modelo.router)
```

6. Reiniciar contenedor
   SQLAlchemy creará automáticamente las tablas nuevas.

---

# 🧠 Cómo añadir campos nuevos a una tabla

1. Modificar modelo SQLAlchemy
2. Borrar `data/app.db` (si estás en desarrollo)
3. Reiniciar contenedor
   → Tablas regeneradas

_(En producción usar Alembic.)_

---

# 🐋 Docker & Volúmenes

El proyecto usa:

```yaml
volumes:
  - ./:/code
  - ./data:/data
```

Lo que permite:

- Editar código en local → cambios inmediatos (por `--reload`)
- Base de datos persistente en `data/app.db`

---

# 🧪 Endpoints por defecto

### GET /

```json
{ "message": "Hello from FastAPI base!" }
```

### POST /users/

Body:

```json
{
  "email": "brian@example.com",
  "nombre": "Brian"
}
```

### GET /users/

Devuelve lista de usuarios.

---

# 🏁 Conclusión

Este proyecto es una base sólida, moderna y extensible para:

- APIs REST profesionales
- Proyectos educativos o de concurso
- Backend para apps Vue/Nuxt/React
- Proyectos más grandes con autenticación, permisos y relaciones complejas

FastAPI + SQLAlchemy + Pydantic v2 + Docker
= **stack ligero, rápido y profesional**.

---

Si quieres, te preparo:

- Autenticación JWT completa
- Relación avanzada 1–N / N–N
- CRUD automático
- Tests con pytest
- Scripts de datos de demo
- Versionado de API (`/api/v1`)

Solo dímelo.
