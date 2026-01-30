from typing import TYPE_CHECKING
from config.config import settings
from main.builders import get_builder
from main.builders.director import Director

if TYPE_CHECKING:
    from fastapi import FastAPI


def create_app():
    builder = get_builder(settings)

    director = Director(builder)

    return director.build_app()


app: "FastAPI" = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main.main:app",
        host=settings.app.host,
        port=settings.app.port,
        workers=settings.app.workers,
        reload=settings.app.debug,
    )
