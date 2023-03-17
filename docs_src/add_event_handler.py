from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


app = Starlette()
app.add_event_handler("startup", database.connect)
app.add_event_handler("shutdown", database.disconnect)
