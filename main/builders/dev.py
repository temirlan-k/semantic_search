from prometheus_fastapi_instrumentator import Instrumentator
import structlog
import logging
from main.builders.base import AbstractAppBuilder
from main.di.container import Container
from src.presentation.http.rest.api.v1 import users, documents, deps, metrics
from src.presentation.http.rest.api.error_handlers import (
    register_error_handlers,
)
from config.config import Environment
from fastapi.middleware.cors import CORSMiddleware


class DevAppBuilder(AbstractAppBuilder):
    def __init__(self, settings):
        super().__init__(settings)
        self.container = None

    def configure_routes(self):
        self.app.include_router(
            users.users_router, prefix="/api/v1/users", tags=["users"]
        )
        self.app.include_router(
            documents.documents_router, prefix="/api/v1/documents", tags=["documents"]
        )
        self.app.include_router(metrics.metrics_router)

    def setup_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def configure_logging(self):
        logging.basicConfig(
            format="%(message)s",
            level=logging.INFO,
        )
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def configure_app_state(self):
        self.app.state.settings = self.settings
        self.app.state.environment = Environment.DEV

        self.app.state.milvus_service = self.container.milvus_service()
        self.app.state.db = self.container.db_adapter()

        self.app.state.to_close_adapters = ["milvus_service", "db"]

        instrumentator = Instrumentator(
            should_group_status_codes=False,
            should_ignore_untemplated=True,
        )
        instrumentator.instrument(self.app).expose(self.app, endpoint="/metrics")

    def configure_exception_handlers(self):
        register_error_handlers(self.app)

    def configure_container(self):
        self.container = Container()
        self.container.wire(modules=[users, documents, deps])
