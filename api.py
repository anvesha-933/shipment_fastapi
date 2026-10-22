from contextlib import asynccontextmanager

from fastapi import FastAPI

from controllers.shipments import router as shipments_router
from controllers.users import router as users_router
from database.sessions import create_db_and_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(title="Shipment Management API", lifespan=lifespan)
app.include_router(users_router)
app.include_router(shipments_router)
