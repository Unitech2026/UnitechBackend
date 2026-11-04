import logging

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import get_engine

logger = logging.getLogger(__name__)

app = FastAPI(title="Unitech - Alumnos")


class Student(BaseModel):
    id: int
    matricula: str
    nombre: str


@app.get(
    "/students",
    response_model=list[Student],
    responses={503: {"description": "No se pudo consultar la base de datos"}},
)
def list_students():
    try:
        with get_engine().connect() as connection:
            students = connection.execute(
                text("SELECT id, matricula, nombre FROM students ORDER BY id")
            ).mappings().all()
        return [Student(**student) for student in students]
    except (SQLAlchemyError, ValueError, ImportError) as error:
        # Los errores de conexión pueden contener credenciales; registrar solo el tipo.
        logger.error("No se pudo consultar students (%s).", type(error).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo consultar la lista de alumnos. Intenta de nuevo más tarde.",
        ) from None
