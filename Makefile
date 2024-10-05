.PHONY: run
run:
	uvicorn python_o_bom_candidato.app:app --host 0.0.0.0 --port 8000

.PHONY: fastapi-run
fastapi-run:
	fastapi run ./python_o_bom_candidato/app.py --port 8000

.PHONY: dev
dev:
	fastapi dev ./python_o_bom_candidato/app.py --port 8000

.PHONY: db
db:
	docker-compose up mongodb

.PHONY: deps-dump
deps-dump:
	poetry export -f requirements.txt --output requirements.txt
