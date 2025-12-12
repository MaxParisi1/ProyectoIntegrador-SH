#!/bin/bash
set -e

echo "Instalando Sistema de Atencion al Cliente - BANCO HENRY"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no esta instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python $PYTHON_VERSION encontrado"

# Crear entorno virtual
if [ -d "venv" ]; then
    echo "El entorno virtual ya existe"
    read -p "Eliminar y crear uno nuevo? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf venv
        echo "Entorno virtual eliminado"
    fi
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Entorno virtual creado"
fi

# Activar entorno virtual y actualizar pip
source venv/bin/activate
echo "Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependencias
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt no encontrado"
    exit 1
fi

echo "Instalando dependencias..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "Error al instalar dependencias"
    exit 1
fi

echo "Dependencias instaladas"

# Configurar archivo .env
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Archivo .env creado. Edita .env y agrega tu GROQ_API_KEY"
    fi
fi

# Crear directorio vectorstore
mkdir -p vectorstore

echo ""
echo "Instalacion completada"
echo ""
echo "Proximos pasos:"
echo "  1. Edita .env con tu API key"
echo "  2. Ejecuta: streamlit run app.py"
echo ""
