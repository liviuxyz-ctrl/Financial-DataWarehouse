from fastapi import FastAPI
from api import assets, data_sources, data
from db.database import initialize_cassandra_connection
import os, sys

app = FastAPI()

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


@app.on_event("startup")
async def on_startup():
    initialize_cassandra_connection()


@app.on_event("shutdown")
async def on_shutdown():
    pass  # Add shutdown logic here if needed


app.include_router(assets.router, prefix="/api/v1", tags=["assets"])
app.include_router(data_sources.router, prefix="/api/v1", tags=["data_sources"])
app.include_router(data.router, prefix="/api/v1", tags=["data"])
