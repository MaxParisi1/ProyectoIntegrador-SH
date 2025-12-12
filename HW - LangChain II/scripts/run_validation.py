#!/usr/bin/env python3
"""
Simple validation runner: ejecuta un conjunto de consultas de prueba
usando `CustomerServiceSystem` y muestra resultados.

Este script está pensado para ejecutarse con el Python del venv:
./venv/bin/python scripts/run_validation.py
"""
import os
import sys
from pathlib import Path

# Asegurar que el proyecto root está en sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from src.main import CustomerServiceSystem

QUERIES = [
    # Balance
    "¿Cuál es el saldo de V-12345678?",
    "Consultar balance de la cédula V-87654321",
    "¿Cuánto dinero tiene la cuenta V-18273645?",
    # Knowledge base
    "¿Cómo puedo abrir una cuenta en BANCO HENRY?",
    "¿Qué necesito para solicitar una tarjeta de crédito?",
    "¿Cuál es el costo de una transferencia internacional?",
    "Información sobre transferencias entre cuentas del mismo banco",
    # General
    "¿Qué es la inflación y cómo afecta mis ahorros?",
    "Explícame la diferencia entre interés simple y compuesto",
    "¿Qué significa tasa de interés?",
]


def main():
    print("Iniciando validacion - CustomerServiceSystem")
    try:
        system = CustomerServiceSystem()
    except Exception as e:
        print("ERROR al inicializar CustomerServiceSystem:", e)
        sys.exit(2)

    results = []
    for i, q in enumerate(QUERIES, 1):
        try:
            res = system.process_query(q)
            results.append((q, res.get("query_type"), res.get("message")))
        except Exception as e:
            results.append((q, "error", f"Exception: {e}"))

    # Imprimir resumen compacto
    print("\n=== Resultados de Validacion ===")
    for i, (q, qtype, msg) in enumerate(results, 1):
        print(f"{i}. Pregunta: {q}")
        print(f"   Tipo: {qtype}")
        print(f"   Respuesta: {msg[:300].replace('\n', ' ')}")
        print("")

    # Resultado general
    errors = [r for r in results if r[1] == "error"]
    if errors:
        print(f"Validacion completada con {len(errors)} errores")
        sys.exit(1)
    else:
        print("Validacion completada: todos los casos procesados correctamente")
        sys.exit(0)


if __name__ == "__main__":
    main()
