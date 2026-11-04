# Unitech — Listado de alumnos

Aplicación full-stack desarrollada como prueba técnica para consultar
un listado de alumnos almacenados en PostgreSQL.

El proyecto utiliza FastAPI para el backend, React para el frontend
y Supabase como servicio de base de datos.

## Aplicación desplegada

- Frontend: https://unitechbackend.pages.dev/
- API: https://unitechbackend-production.up.railway.app/students
- Documentación de la API: https://unitechbackend-production.up.railway.app/docs
- Repositorio: https://github.com/Unitech2026/UnitechBackend

## Tecnologías utilizadas

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)
- Psycopg 3
- Alembic
- uv
- Ruff

### Frontend

- React
- Vite
- JavaScript
- ESLint

### Infraestructura

- Supabase: base de datos PostgreSQL
- Railway: despliegue del backend
- Cloudflare Pages: despliegue del frontend
- GitHub Actions: integración continua

## Estructura del proyecto

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── frontend/
│   ├── .env.example
│   ├── src/
│   ├── package.json
│   └── package-lock.json
├── migrations/
│   ├── versions/
│   └── env.py
├── tests/
│   └── test_students.py
├── .env.example
├── .gitignore
├── .python-version
├── alembic.ini
├── database.py
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Instalación y ejecución local

### Requisitos

- Python 3.12 o superior
- uv
- Node.js 24 (la misma versión utilizada en CI)
- npm
- Acceso a una base de datos PostgreSQL

### 1. Clonar el repositorio

```bash
git clone https://github.com/Unitech2026/UnitechBackend.git
cd UnitechBackend
```

### 2. Configurar el backend

Instalar las dependencias:

```bash
uv sync --locked
```

Crear el archivo de variables de entorno:

```bash
cp .env.example .env
```

Editar `.env` y configurar la conexión PostgreSQL:

```dotenv
DATABASE_URL=postgresql+psycopg://USUARIO:CONTRASENA@HOST:5432/postgres?sslmode=require
```

Reemplazar los valores de ejemplo por las credenciales correspondientes.

Si la contraseña contiene caracteres especiales reservados en una URL,
deben codificarse correctamente.

### 3. Ejecutar las migraciones

Aplicar las migraciones pendientes:

```bash
uv run alembic upgrade head
```

La migración inicial crea la tabla `students` con los campos:

| Campo | Tipo | Restricciones |
|-------|------|---------------|
| id | Integer | Clave primaria |
| matricula | String(20) | Único y obligatorio |
| nombre | String(100) | Obligatorio |

Además, inserta 10 alumnos de ejemplo.

Para consultar la revisión aplicada:

```bash
uv run alembic current
```

### 4. Iniciar el backend

```bash
uv run --env-file .env uvicorn main:app --reload
```

La API estará disponible en:

- http://127.0.0.1:8000/students
- http://127.0.0.1:8000/docs

### 5. Configurar el frontend

Desde la raíz del repositorio:

```bash
cd frontend
npm ci
```

Crear el archivo local desde el ejemplo:

```bash
cp .env.example .env
```

El archivo `frontend/.env` debe contener:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

Esta variable indica la dirección del backend que utilizará React. Es pública y se incorpora durante la compilación. No debe contener credenciales ni terminar en `/students`. Reinicia Vite después de cambiarla.

Vite detiene el inicio o la compilación si falta esta variable o no es una URL HTTP o HTTPS válida. Las barras finales se normalizan para evitar rutas con `//students`.

También puede configurarse con la URL pública de Railway
si se desea consumir la API desplegada.

### 6. Iniciar el frontend

```bash
npm run dev
```

Abrir la dirección mostrada por Vite, normalmente:

http://localhost:5173/

La aplicación consultará el endpoint `/students` y mostrará
los alumnos en una tabla.

## API

### GET /students

Devuelve el listado de alumnos ordenado por `id`.

**Respuesta exitosa: HTTP 200**

```json
[
  {
    "id": 1,
    "matricula": "20260001",
    "nombre": "Alumno 1"
  },
  {
    "id": 2,
    "matricula": "20260002",
    "nombre": "Alumno 2"
  }
]
```

La migración inicial inserta un total de 10 registros.

Si no existen alumnos, el endpoint devuelve un arreglo vacío:

```json
[]
```

**Error de base de datos: HTTP 503**

Si no se puede establecer la conexión o ejecutar la consulta,
la API devuelve un mensaje genérico sin exponer credenciales
ni información interna.

## Validaciones

### Backend

Ejecutar el linter:

```bash
uv run ruff check .
```

Verificar la sintaxis:

```bash
uv run python -m compileall -q main.py database.py migrations
```

Ejecutar las pruebas de migración, restricciones y consulta de alumnos:

```bash
uv run python -m unittest discover -s tests -v
```

Por defecto, las pruebas crean una base SQLite temporal. En CI se ejecutan sobre un servicio PostgreSQL 17 temporal mediante `TEST_DATABASE_URL`. Esta variable debe apuntar exclusivamente a una base desechable: las pruebas crean y eliminan la tabla `students`. Las pruebas no utilizan el `DATABASE_URL` de `.env` como destino.

Comprobar las revisiones disponibles de Alembic (este comando solo muestra el historial, no aplica migraciones):

```bash
uv run alembic heads
```

### Frontend

Desde el directorio `frontend`:

```bash
npm run lint
npm run build
```

El comando `build` genera los archivos de producción en `frontend/dist`.

## Integración continua

El proyecto utiliza GitHub Actions mediante el workflow:

`.github/workflows/ci.yml`

Se ejecuta automáticamente cuando:

- Se envían cambios a cualquier rama.
- Se crea o actualiza un pull request.

El workflow contiene dos trabajos independientes:

**Backend**

- Instalación de Python y dependencias con uv.
- Análisis estático con Ruff.
- Verificación de sintaxis.
- Comprobación de revisiones de Alembic.
- Pruebas con PostgreSQL 17: creación de tabla y 10 alumnos, restricciones, reversión de la migración, lista vacía y manejo de errores.

**Frontend**

- Instalación de Node.js y dependencias.
- Análisis estático con ESLint.
- Compilación de producción con Vite usando una URL de API de ejemplo. Este build de validación no se publica; Cloudflare debe compilar con la URL real de Railway.

Estas verificaciones no modifican la base de datos de producción.

Crear el workflow no configura por sí solo los servicios de despliegue. En Railway, activa [Wait for CI](https://docs.railway.com/deployments/github-autodeploys#wait-for-ci) para que espere los resultados de GitHub Actions.

La [integración Git de Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/git-integration/) despliega por su cuenta. Para exigir ambos jobs antes de publicar, desactiva sus despliegues automáticos y publica con Wrangler desde un job de GitHub Actions dependiente de `backend` y `frontend`. Esto requiere configurar las credenciales de Cloudflare en GitHub; este repositorio todavía no configura ese paso de publicación.

## Despliegue

### Backend — Railway

El backend se despliega desde el repositorio de GitHub.

Configuración necesaria:

- Variable de entorno: `DATABASE_URL`
- Variable opcional: `CORS_ORIGINS`, con los orígenes permitidos separados por comas, sin barra final. Por defecto se permiten `http://localhost:5173`, `http://127.0.0.1:5173` y `https://unitechbackend.pages.dev`.
- Base de datos: PostgreSQL en Supabase

Comando previo al despliegue, para aplicar las migraciones versionadas:

```bash
uv run alembic upgrade head
```

Comando de inicio:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port "$PORT"
```

URL pública:

https://unitechbackend-production.up.railway.app/students

### Frontend — Cloudflare Pages

El frontend se despliega desde el mismo repositorio.

Configuración:

| Propiedad | Valor |
|-----------|-------|
| Rama de producción | main |
| Directorio raíz | frontend |
| Comando de compilación | npm run build |
| Directorio de salida | dist |

Variable de entorno de compilación:

```dotenv
VITE_API_URL=https://unitechbackend-production.up.railway.app
```

URL pública:

https://unitechbackend.pages.dev/

## Seguridad

- Las credenciales se almacenan en variables de entorno.
- Los archivos `.env` no deben incluirse en el repositorio.
- `.env.example` contiene únicamente valores de ejemplo.
- La API evita devolver detalles internos ante errores de conexión.
- La variable `VITE_API_URL` es pública y no contiene credenciales.
- Guarda el `.env` del frontend en `frontend/`, nunca en `frontend/public/`: los archivos públicos se copian al despliegue.
- CORS limita los orígenes del navegador; no sustituye autenticación ni autorización.

## Autor

Desarrollado como parte de la evaluación técnica de Unitech.
