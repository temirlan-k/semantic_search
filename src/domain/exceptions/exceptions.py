class EntityNotFoundException(Exception):
    """Not found."""

    pass


class EntityAlreadyExistsException(Exception):
    """Already exists."""

    pass


class InvalidCredentialsException(Exception):
    """Invalid credentials."""

    pass


class UnauthorizedException(Exception):
    """
    Unauthorized
    """

    pass


class DocumentProcessingException(Exception):
    """Ошибка при обработке документа (парсинг, чанкинг)"""

    pass


class LLMServiceException(Exception):
    """Ошибка при обращении к LLM сервису (Ollama)"""

    pass


class VectorDBException(Exception):
    """Ошибка при работе с векторной базой данных (Milvus)"""

    pass
