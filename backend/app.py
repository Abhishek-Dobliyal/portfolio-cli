from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from router.routes import close_database, initialize_database, router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    try:
        yield
    finally:
        close_database()


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router=router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.get_frontend_origin()],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
    return app


app = create_app()
