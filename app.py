from blacksheep import Application, json, Router
from sqlalchemy import Column, Integer
from sqlalchemy import Table, Unicode, select, MetaData, insert
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/gone"

METADATA = MetaData()
REDIRECTS = Table(
    "paths",
    METADATA,
    Column("path", Unicode, primary_key=True),
    Column("status", Integer),
)

api = Router()
app = Application(router=api)
engine = create_async_engine(DATABASE_URL, future=True)


@api.get("/-")
async def health_check():
    return json({"data": {"message": "OK"}})


@api.get("/status")
async def get_status(db: AsyncConnection):
    async with db as t:
        r = await t.execute(select(REDIRECTS.c.status))
        entries = r.all()
        return json([{"path": entry.path, "status": entry.status} for entry in entries])


@api.post("/status/{name}")
async def post_status(db: AsyncConnection, name: str):
    async with db as t:
        await t.execute(insert(REDIRECTS), [{"path": name, "status": 410}])
    return json({"data": {"message": "Imported"}}, 201)


async def dispose_db(_):
    await engine.dispose()


def create_connection():
    return engine.begin()


async def _initialize_db(_, drop=False):
    print("Initializing the database")
    async with create_connection() as t:
        if drop:
            await t.run_sync(METADATA.drop_all)
        await t.run_sync(METADATA.create_all)
    await dispose_db(None)


def configure_service():
    print("Configuring the service")
    app.on_start += _initialize_db
    app.on_stop += dispose_db

    app.services.add_scoped_by_factory(create_connection, AsyncConnection)
    app.services.add_alias("db", AsyncConnection)


print("Starting the app")
configure_service()
