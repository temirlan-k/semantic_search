from abc import ABC, abstractmethod
from fastapi import FastAPI


class AbstractAppBuilder(ABC):
    
    def __init__(self, settings):
        self.settings = settings
        self.app = FastAPI()
    
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