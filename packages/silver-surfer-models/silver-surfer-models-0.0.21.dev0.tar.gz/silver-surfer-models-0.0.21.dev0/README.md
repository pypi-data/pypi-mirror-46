## silver-surfer-db-models

This package provides a reusable abstraction to connect to the silver surfer
database.

### Commands

**List commands**

`inv -l`

### Usage

**Configure the database in your app**

```
from silver_surfer_models.database import get_db_session

db_uri = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
    'root',
    'password',
    'host',
    'db',
)
engine, db_session, Base = database.get_db_session(db_uri)

```

### How to release a new version?

**Update the `version` in `setup.py`**

```
setuptools.setup(
    ...
    version='0.0.9',
    ...
)
```

**Build the wheel**

```inv build```

**Upload the wheel to PyPi repository**

```inv push```
