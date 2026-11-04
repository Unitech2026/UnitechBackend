"""create_students_table

Revision ID: 83aaaed42dfc
Revises: 
Create Date: 2026-11-04 10:24:45.178515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83aaaed42dfc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    students = op.create_table(
        "students",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("matricula", sa.String(20), unique=True, nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
    )

    op.bulk_insert(
        students,
        [
            {
                "matricula": f"202600{i:02d}",
                "nombre": f"Alumno {i}"
            }
            for i in range(1, 11)
        ]
    )



def downgrade():
    op.drop_table("students")