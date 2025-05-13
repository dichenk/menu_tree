# Makefile для проекта Django на uv в структуре src/

# Путь к manage.py
MANAGE=uv run python src/manage.py

.PHONY: run migrate makemigrations shell createsuperuser test format

run:
	$(MANAGE) runserver 8001

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

shell:
	$(MANAGE) shell

createsuperuser:
	$(MANAGE) createsuperuser

test:
	$(MANAGE) test

format:
	uv run black src/ apps/
	uv run isort src/ apps/

newapp:
	mkdir -p src/apps/$(name)
	$(MANAGE) startapp $(name) src/apps/$(name)
