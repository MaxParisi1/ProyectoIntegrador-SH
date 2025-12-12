#!/bin/bash
set -e

if [ ! -d "venv" ]; then
    echo "Error: Entorno virtual no encontrado"
    echo "Ejecuta: ./install.sh"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "Error: Archivo .env no encontrado"
    echo "Ejecuta: cp .env.example .env"
    exit 1
fi

echo "Iniciando aplicacion..."
./venv/bin/streamlit run app.py
