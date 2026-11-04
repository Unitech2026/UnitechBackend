import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alembic import command
from alembic.config import Config
from fastapi import HTTPException
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError, OperationalError

from database import get_engine
from main import list_students

ROOT = Path(__file__).resolve().parents[1]


class StudentsTests(unittest.TestCase):
    def setUp(self):
        temporary_directory = self.enterContext(tempfile.TemporaryDirectory())
        # Nunca tomar DATABASE_URL ni .env como destino de las pruebas.
        database_url = os.getenv("TEST_DATABASE_URL") or (
            "sqlite:///" + str(Path(temporary_directory) / "students.db")
        )
        self.enterContext(patch.dict(os.environ, {"DATABASE_URL": database_url}))
        self.config = Config(str(ROOT / "alembic.ini"))
        get_engine.cache_clear()
        command.upgrade(self.config, "head")
        self.engine = get_engine()
        self.addCleanup(self.engine.dispose)
        self.addCleanup(get_engine.cache_clear)
        self.addCleanup(command.downgrade, self.config, "base")

    def test_migration_seeds_ten_students(self):
        students = list_students()
        self.assertEqual(len(students), 10)
        self.assertEqual(len({student.matricula for student in students}), 10)
        self.assertEqual([student.id for student in students], list(range(1, 11)))
        self.assertEqual(
            students[0].model_dump(),
            {"id": 1, "matricula": "20260001", "nombre": "Alumno 1"},
        )
        self.assertTrue(all(student.nombre for student in students))

    def test_database_rejects_duplicate_and_null_values(self):
        cases = [
            {"matricula": "20260001", "nombre": "Duplicado"},
            {"matricula": None, "nombre": "Sin matrícula"},
            {"matricula": "PRUEBA", "nombre": None},
        ]
        for values in cases:
            with (
                self.subTest(values=values),
                self.assertRaises(IntegrityError),
                self.engine.begin() as connection,
            ):
                connection.execute(
                    text(
                        "INSERT INTO students (matricula, nombre) "
                        "VALUES (:matricula, :nombre)"
                    ),
                    values,
                )

    def test_empty_table_returns_empty_list(self):
        with self.engine.begin() as connection:
            connection.execute(text("DELETE FROM students"))
        self.assertEqual(list_students(), [])

    def test_migration_can_be_reverted_and_reapplied(self):
        command.downgrade(self.config, "base")
        self.assertNotIn("students", inspect(self.engine).get_table_names())
        command.upgrade(self.config, "head")
        command.upgrade(self.config, "head")
        self.assertEqual(len(list_students()), 10)

    def test_database_error_returns_generic_503(self):
        secret = "CLAVE_FICTICIA_NO_PUBLICAR"
        error = OperationalError("SELECT", {}, Exception(secret))
        with (
            patch("main.get_engine", side_effect=error),
            self.assertLogs("main", level="ERROR") as logs,
            self.assertRaises(HTTPException) as caught,
        ):
            list_students()
        self.assertEqual(caught.exception.status_code, 503)
        self.assertNotIn(secret, caught.exception.detail)
        self.assertNotIn(secret, "\n".join(logs.output))

    def test_missing_configuration_returns_503(self):
        with patch.dict(os.environ, {"DATABASE_URL": ""}):
            get_engine.cache_clear()
            with (
                self.assertLogs("main", level="ERROR"),
                self.assertRaises(HTTPException) as caught,
            ):
                list_students()
        self.assertEqual(caught.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()
