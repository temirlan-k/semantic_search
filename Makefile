OLLAMA_MODEL=nomic-embed-text

.PHONY: up ollama_pull

up:
	docker-compose up -d
	@echo "Ждем Ollama..."
	@sleep 5
	make ollama_pull

ollama_pull:
	docker-compose exec ollama ollama pull $(OLLAMA_MODEL)
