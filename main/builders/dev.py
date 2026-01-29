import logging
from main.builders.base import AbstractAppBuilder
from main.di.container import Container
from src.presentation.http.rest.api.v1 import users
from src.presentation.http.rest.api.error_handlers.error_handlers import register_error_handlers
from config.config import Environment
from dependency_injector import containers, providers

class DevAppBuilder(AbstractAppBuilder):

    
    def configure_routes(self):
        self.app.include_router(users.users_router, prefix="/api/v1/users", tags=["users"])
    
    def setup_middlewares(self):
        from fastapi.middleware.cors import CORSMiddleware

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def configure_logging(self):
        pass
    
    def configure_app_state(self):
        self.app.state.settings = self.settings
        self.app.state.environment = Environment.DEV

    def configure_exception_handlers(self):
        register_error_handlers(self.app)

    def configure_container(self):
        container = Container()
        container.wire(
            modules=[
                users,
            ]
        )

        self.app.container = container