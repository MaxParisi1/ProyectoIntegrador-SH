VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
STREAMLIT := $(VENV)/bin/streamlit
PYTEST := $(VENV)/bin/pytest

.PHONY: help setup run test validate clean

.DEFAULT_GOAL := help

help:
	@echo "Sistema de Atencion al Cliente - BANCO HENRY"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make setup      Instala dependencias y configura el proyecto"
	@echo "  make run        Ejecuta la aplicacion Streamlit"
	@echo "  make test       Ejecuta los tests"
	@echo "  make validate   Ejecuta validacion de 10 consultas (scripts/validate.sh)"
	@echo "  make clean      Limpia archivos temporales"
	@echo ""

setup:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creando entorno virtual..."; \
		python3 -m venv $(VENV); \
	fi
	@echo "Instalando dependencias..."
	@$(PIP) install --upgrade pip --quiet
	@$(PIP) install -r requirements.txt --quiet
	@if [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "Archivo .env creado. Edita .env y agrega tu GROQ_API_KEY"; \
	fi
	@mkdir -p vectorstore
	@echo "Setup completado"

run:
	@$(STREAMLIT) run app.py

test:
	@$(PYTEST) tests/ -v

validate:
	@$(PYTHON) scripts/run_validation.py

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Limpieza completada"
