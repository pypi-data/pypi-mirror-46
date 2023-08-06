import datetime
from typing import Iterable, Optional, List

import sqlalchemy as sa
from monkeytype.db.base import CallTraceStore, CallTraceThunk
from monkeytype.encoding import CallTraceRow, serialize_traces
from monkeytype.tracing import CallTrace

metadata = sa.MetaData()

trace_table = sa.Table(
    "monkeytype_call_traces",
    metadata,
    sa.Column("created_at", sa.TEXT()),
    sa.Column("module", sa.TEXT()),
    sa.Column("qualname", sa.TEXT()),
    sa.Column("arg_types", sa.TEXT()),
    sa.Column("return_type", sa.TEXT()),
    sa.Column("yield_type", sa.TEXT()),
)


class SQLAlchemyStore(CallTraceStore):
    def __init__(self, engine: sa.engine.Engine):
        self.engine = engine

    @classmethod
    def make_store(cls, connection_string: str) -> CallTraceStore:
        """Create a new store instance.

        This is a factory function that is intended to be used by the CLI.
        """
        engine = sa.create_engine(connection_string)
        metadata.create_all(engine)
        return cls(engine)

    def add(self, traces: Iterable[CallTrace]) -> None:
        with self.engine.connect() as conn:
            conn.execute(
                trace_table.insert(),
                [
                    {
                        "created_at": datetime.datetime.now(),
                        "module": row.module,
                        "qualname": row.qualname,
                        "arg_types": row.arg_types,
                        "return_type": row.return_type,
                        "yield_type": row.yield_type,
                    }
                    for row in serialize_traces(traces)
                ],
            )

    def filter(self, module: str, qualname_prefix: Optional[str] = None, limit: int = 2000) -> List[CallTraceThunk]:
        with self.engine.connect() as conn:
            query = sa.select(
                [
                    trace_table.c.module,
                    trace_table.c.qualname,
                    trace_table.c.arg_types,
                    trace_table.c.return_type,
                    trace_table.c.yield_type,
                ]
            ).distinct()
            query = query.where(trace_table.c.module == module)
            if qualname_prefix:
                query = query.where(trace_table.c.qualname.like(sa.func.concat(qualname_prefix, "%")))
            query = query.order_by(trace_table.c.created_at.desc())
            query = query.limit(limit)

            return [CallTraceRow(*row) for row in conn.execute(query)]

    def list_modules(self) -> List[str]:
        with self.engine.connect() as conn:
            query = sa.select([trace_table.c.module]).distinct()
            query = query.order_by(trace_table.c.created_at.desc())
            results = [module or "" for (module,) in conn.execute(query)]

            return results
