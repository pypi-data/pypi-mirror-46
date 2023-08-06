## Monkeytype SQLAlchemy

A SQLAlchemy-backed store for use with [monkeytype](https://github.com/Instagram/MonkeyType) by Instagram.

This store is schema-compatible with the default SQLite-backend store, merely using SQLAlchemy for database 
 interactions. This allows easy use of any 
 [database dialect supported by SQLAlchemy](https://docs.sqlalchemy.org/en/13/dialects/index.html)
 
### Usage

Create a `monkeytype_config.py` in your project folder as suggested by the MonkeyType docs

```python
from monkeytype_sqlalchemy import SQLAlchemyConfig

CONFIG = SQLAlchemyConfig()
```

Alternately, modify your Config class to return an instance of the `SQLAlchemyStore` call trace store

```python
from monkeytype.config import Config
from monkeytype.db.base import CallTraceStore
from monkeytype_sqlalchemy import SQLAlchemyStore

class MyConfig(Config):
    def trace_store(self) -> CallTraceStore:
        return SQLAlchemyStore.make_store("postgresql+psycopg:///localhost/my_database")
```
