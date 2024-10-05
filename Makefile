.PHONY: run
run:
	fastapi run ./python_o_bom_candidato/app.py --port 8000

.PHONY: dev
dev:
	fastapi dev ./python_o_bom_candidato/app.py --port 8000

.PHONY: db
db:
	docker-compose up mongodb
