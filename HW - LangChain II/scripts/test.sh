#!/bin/bash
set -e

if [ ! -d "venv" ]; then
    echo "Error: Entorno virtual no encontrado"
    echo "Ejecuta: ./install.sh"
    exit 1
fi

echo "Ejecutando tests..."
./venv/bin/pytest tests/ -v "$@"
