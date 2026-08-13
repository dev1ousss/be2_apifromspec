from datasource.database import Base, engine
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from web.routers import (
    addresses_router,
    clients_router,
    images_router,
    product_router,
    suppliers_router,
)

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Shop API",
    version="1.0.0",
    description="API для управления магазином (товары, клиенты, адреса)",
    docs_url=None,
    redoc_url=None,
)


@app.get("/swagger/index.html", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
    )


app.include_router(addresses_router, prefix="/api/v1")
app.include_router(clients_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")
app.include_router(suppliers_router, prefix="/api/v1")
