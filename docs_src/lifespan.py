from contextlib import asynccontextmanager

from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


@asynccontextmanager
async def lifespan(app: Starlette):
    # On startup
    await database.connect()
    yield
    # On shutdown
    await database.disconnect()


app = Starlette(lifespan=lifespan)
