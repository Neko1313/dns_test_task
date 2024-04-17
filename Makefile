# Bash
dev:
	docker-compose -f docker-compose.dev.yml up --build --force-recreate

test:
	docker-compose -f docker-compose.test.yml up --build --force-recreate