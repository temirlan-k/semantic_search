OLLAMA_MODEL=nomic-embed-text

.PHONY: up ollama_pull down install run test lint clean

# Docker commands
up:
	docker-compose up -d
	@echo "Ждем Ollama..."
	@sleep 5
	make ollama_pull

ollama_pull:
	docker-compose exec ollama ollama pull $(OLLAMA_MODEL)

down:
	docker-compose down -v

# Local development commands
install:
	uv sync

test:
	uv run pytest tests -vv

lint:
	uvx ruff check

format:
	uvx ruff format
