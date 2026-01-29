from abc import ABC, abstractmethod
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
import structlog
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger = structlog.get_logger()
    
    state = app.state
    logger.info("Application starting")
    
    for adapter_name in getattr(state, "to_close_adapters", []):
        adapter: Optional[object] = getattr(state, adapter_name, None)
        if adapter is not None and hasattr(adapter, 'connect'):
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(1, max_retries + 1):
                try:
                    await adapter.connect()
                    logger.info(f"{adapter_name} connected", status="ready", attempt=attempt)
                    break
                except Exception as e:
                    if attempt == max_retries:
                        logger.error(f"{adapter_name} connect failed after {max_retries} attempts", error=str(e))
                        raise
                    logger.warning(f"{adapter_name} connect failed", 
                                 attempt=attempt, 
                                 max_retries=max_retries,
                                 retry_in_seconds=retry_delay)
                    await asyncio.sleep(retry_delay)
    
    yield  # Request handling
    
    logger.info("Application shutting down")
    for adapter_name in getattr(state, "to_close_adapters", []):
        adapter: Optional[object] = getattr(state, adapter_name, None)
        if adapter is not None:
            try:
                await adapter.close()
                logger.info(f"{adapter_name} closed", status="close")
            except Exception as e:
                logger.error(f"{adapter_name} close failed", error=str(e))


class AbstractAppBuilder(ABC):
    def __init__(self, settings):
        self.settings = settings
        self.app = FastAPI(lifespan=lifespan)

    @abstractmethod
    def configure_routes(self):
        pass

    @abstractmethod
    def setup_middlewares(self):
        pass

    @abstractmethod
    def configure_logging(self):
        pass

    @abstractmethod
    def configure_app_state(self):
        pass

    @abstractmethod
    def configure_exception_handlers(self):
        pass

    @abstractmethod
    def configure_container(self):
        pass