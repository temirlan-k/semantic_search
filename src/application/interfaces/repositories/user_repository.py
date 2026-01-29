from abc import ABC, abstractmethod

class IUserRepository(ABC):
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def create_user(self, user_data):
        raise NotImplementedError
    
    @abstractmethod
    async def update_user(self, user_id: str, user_data):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_user(self, user_id: str):
        raise NotImplementedError
