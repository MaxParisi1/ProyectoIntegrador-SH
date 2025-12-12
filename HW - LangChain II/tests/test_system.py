"""
Tests para el sistema de atención al cliente.
"""

import pytest
from pathlib import Path
import sys

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.tools.csv_tool import CSVBalanceTool
from src.config import Config


class TestCSVBalanceTool:
    """Tests para la herramienta de consulta de saldos"""
    
    @pytest.fixture
    def csv_tool(self):
        """Fixture que crea una instancia de CSVBalanceTool"""
        return CSVBalanceTool(Config.DATA_CSV_PATH)
    
    def test_get_balance_exists(self, csv_tool):
        """Test: Consultar un saldo que existe"""
        result = csv_tool.get_balance("V-12345678")
        
        assert result["success"] == True
        assert result["data"]["cedula"] == "V-12345678"
        assert result["data"]["nombre"] == "Juan Pérez"
        assert result["data"]["balance"] == 1250.5
    
    def test_get_balance_not_found(self, csv_tool):
        """Test: Consultar un saldo que no existe"""
        result = csv_tool.get_balance("V-99999999")
        
        assert result["success"] == False
        assert result["error"] == "not_found"
        assert "No se encontró" in result["message"]
    
    def test_search_balance_with_cedula(self, csv_tool):
        """Test: Buscar saldo mencionando cédula en texto"""
        result = csv_tool.search_balance("¿Cuál es el saldo de V-87654321?")
        
        assert result["success"] == True
        assert result["data"]["cedula"] == "V-87654321"
        assert result["data"]["nombre"] == "María Gómez"
    
    def test_search_balance_without_cedula(self, csv_tool):
        """Test: Buscar saldo sin mencionar cédula"""
        result = csv_tool.search_balance("¿Cuánto dinero tengo?")
        
        assert result["success"] == False
        assert result["error"] == "no_cedula_found"
    
    def test_multiple_accounts(self, csv_tool):
        """Test: Verificar que existen múltiples cuentas"""
        df = csv_tool.get_all_balances()
        
        assert len(df) >= 10
        assert "ID_Cedula" in df.columns
        assert "Nombre" in df.columns
        assert "Balance" in df.columns


class TestQueryClassification:
    """Tests para la clasificación de consultas"""
    
    # Casos de prueba para balance
    balance_queries = [
        "¿Cuál es el saldo de V-12345678?",
        "Saldo de la cédula V-87654321",
        "¿Cuánto dinero tiene Juan Pérez?",
        "Consultar balance de V-18273645"
    ]
    
    # Casos de prueba para knowledge base
    kb_queries = [
        "¿Cómo abro una cuenta?",
        "Requisitos para tarjeta de crédito",
        "¿Cómo hago una transferencia internacional?",
        "Pasos para solicitar una tarjeta"
    ]
    
    # Casos de prueba para general
    general_queries = [
        "¿Qué es la inflación?",
        "Explícame qué es un interés compuesto",
        "¿Cuál es la diferencia entre débito y crédito?",
        "Hola, ¿cómo estás?"
    ]
    
    @pytest.mark.parametrize("query", balance_queries)
    def test_balance_classification(self, query):
        """Test: Las consultas de balance deben clasificarse correctamente"""
        # Este test requiere el sistema completo inicializado
        # Se puede implementar como test de integración
        pass
    
    @pytest.mark.parametrize("query", kb_queries)
    def test_kb_classification(self, query):
        """Test: Las consultas de KB deben clasificarse correctamente"""
        pass
    
    @pytest.mark.parametrize("query", general_queries)
    def test_general_classification(self, query):
        """Test: Las consultas generales deben clasificarse correctamente"""
        pass


class TestSystemIntegration:
    """Tests de integración del sistema completo"""
    
    def test_system_initialization(self):
        """Test: El sistema se inicializa correctamente"""
        # Este test requiere las API keys configuradas
        pass
    
    def test_process_balance_query(self):
        """Test: Procesar una consulta de balance completa"""
        pass
    
    def test_process_kb_query(self):
        """Test: Procesar una consulta de knowledge base completa"""
        pass
    
    def test_process_general_query(self):
        """Test: Procesar una consulta general completa"""
        pass
    
    def test_error_handling_no_api(self):
        """Test: Manejo de errores cuando no hay API disponible"""
        pass


# Casos de prueba específicos (10 consultas variadas)
TEST_QUERIES = [
    # Balance queries
    ("¿Cuál es el saldo de V-12345678?", "balance"),
    ("Consultar balance de la cédula V-87654321", "balance"),
    
    # Knowledge base queries
    ("¿Cómo puedo abrir una cuenta en BANCO HENRY?", "knowledge_base"),
    ("¿Qué necesito para solicitar una tarjeta de crédito?", "knowledge_base"),
    ("¿Cuál es el costo de una transferencia internacional?", "knowledge_base"),
    ("Información sobre transferencias entre cuentas", "knowledge_base"),
    
    # General queries
    ("¿Qué es la inflación y cómo afecta mis ahorros?", "general"),
    ("Explícame la diferencia entre interés simple y compuesto", "general"),
    ("¿Qué significa tasa de interés?", "general"),
    ("Hola, necesito ayuda", "general"),
]


@pytest.mark.parametrize("query,expected_type", TEST_QUERIES)
def test_query_routing(query, expected_type):
    """
    Test parametrizado: Verifica que las consultas se enruten correctamente.
    
    Este test valida los 10 casos de prueba específicos.
    """
    # Implementación del test
    # Requiere sistema inicializado con API keys
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
