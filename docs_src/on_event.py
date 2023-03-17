from saffier import Database, Registry

from starlette_bridge import Starlette

database = Database("sqlite:///db.sqlite")
models = Registry(database=database)


app = Starlette()


@app.on_event("startup")
async def start_database():
    await database.connect()


@app.on_event("shutdown")
async def close_database():
    await database.disconnect()
