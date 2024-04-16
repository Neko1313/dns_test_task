# Bash
dev:
	docker-compose -f docker-compose.yml up --build --force-recreate

test:
	docker exec -it $(docker-compose ps -q api) /bin/bash -c "pytest test_api.py"