
from main.builders.base import AbstractAppBuilder
from fastapi import FastAPI


class Director:
    def __init__(self, builder: AbstractAppBuilder):
        self._builder = builder

    def build_app(self) -> FastAPI:
        self._builder.configure_routes()
        self._builder.setup_middlewares()
        self._builder.configure_logging()
        self._builder.configure_app_state()
        self._builder.configure_exception_handlers()
        self._builder.configure_container()
        return self._builder.app