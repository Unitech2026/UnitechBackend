# Backend Unitech

API en Python con FastAPI para consultar alumnos en PostgreSQL.

## Ejecutar localmente

Requisitos: Python 3.12 o superior y uv.

1. Instala las dependencias con `uv sync --locked`.
2. Copia `.env.example` a `.env` y configura `DATABASE_URL` con la conexión de Supabase. Si la contraseña contiene caracteres especiales, deben estar codificados para una URL.
3. Inicia la API:

   ```bash
   uv run --env-file .env uvicorn main:app --reload
   ```

Consulta `http://127.0.0.1:8000/students` o abre la documentación interactiva en `http://127.0.0.1:8000/docs`.

La tabla `students` debe existir y tener aplicada la migración del proyecto. La configuración de Alembic para leer `DATABASE_URL` todavía está pendiente; este comando solo inicia la API.

## Consultar alumnos

`GET /students` devuelve un arreglo JSON ordenado por `id`:

```json
[
  {"id": 1, "matricula": "20260001", "nombre": "Alumno 1"}
]
```

Si la tabla está vacía, devuelve `[]`. Si falta la configuración o falla la consulta, responde con HTTP 503 y un mensaje genérico, sin exponer credenciales ni detalles internos.

En Railway, configura `DATABASE_URL` como variable de entorno y usa como comando de inicio:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port "$PORT"
```

No subas `.env` ni claves privadas al repositorio. `.env.example` contiene únicamente valores ficticios.
