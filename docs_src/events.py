from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


app = Starlette(
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
