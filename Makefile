reopen:
	docker system prune -f
	docker-compose up --build
open:
	docker-compose up --build