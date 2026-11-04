import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL no está configurada.")

    url = make_url(database_url)
    if url.drivername in {"postgres", "postgresql"}:
        url = url.set(drivername="postgresql+psycopg")

    connect_args = {}
    if url.get_backend_name() == "postgresql":
        connect_args["connect_timeout"] = 10

    return create_engine(
        url,
        pool_pre_ping=True,
        hide_parameters=True,
        connect_args=connect_args,
    )
