from datasource.database import Base, engine
from fastapi import FastAPI
from web.routers import (
    addresses_router,
    clients_router,
    images_router,
    product_router,
    suppliers_router,
)

Base.metadata.create_all(bind=engine)


app = FastAPI(title="shopapi", version="1.0.0")

#
# @app.get("/")
# def read_root():
#     return {"status": "ok", "message": "Database initialized successfully"}


app.include_router(addresses_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")
app.include_router(suppliers_router, prefix="/api/v1")
