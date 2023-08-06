import os

from monkeytype.config import DefaultConfig
from monkeytype.db.base import CallTraceStore

from monkeytype_sqlalchemy import SQLAlchemyStore


class SQLAlchemyConfig(DefaultConfig):
    def trace_store(self) -> CallTraceStore:
        db_path = os.environ.get(self.DB_PATH_VAR, "sqlite:///monkeytype.sqlite3")

        return SQLAlchemyStore.make_store(db_path)
