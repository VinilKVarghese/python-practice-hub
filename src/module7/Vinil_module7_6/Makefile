
# Build the Streamlit Docker image
build:
	docker compose build

# Start Ollama and Streamlit
up:
	docker compose up -d

# Download the Qwen model
pull:
	docker compose exec ollama ollama pull qwen2.5:1.5b

# Show running containers
ps:
	docker compose ps

# Show application logs
logs:
	docker compose logs -f chat-app

# Stop containers without deleting stored data
stop:
	docker compose stop

# Stop and remove containers, keeping volumes
down:
	docker compose down

# Remove containers and stored volumes
clean:
	docker compose down -v