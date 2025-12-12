"""
Router inteligente para clasificar y enrutar consultas de usuarios.
"""

from typing import Dict, Literal
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

QueryType = Literal["balance", "knowledge_base", "general"]


class QueryRouter:
    """Router que clasifica consultas y las dirige a la herramienta apropiada"""
    
    def __init__(self, api_key: str, model: str):
        """
        Inicializa el router.
        
        Args:
            api_key: API key de Groq
            model: Nombre del modelo a usar
        """
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=0.1  # Temperatura baja para clasificación consistente
        )
        
        self.classification_prompt = PromptTemplate(
            input_variables=["query"],
            template="""Eres un clasificador de consultas para un sistema bancario. 

Analiza la siguiente consulta del usuario y clasifícala en UNA de estas categorías:

1. "balance" - Si el usuario pregunta por saldo, balance, dinero en cuenta, o menciona un número de cédula/identificación
   Ejemplos: "¿Cuál es mi saldo?", "Saldo de V-12345678", "¿Cuánto dinero tengo?"

2. "knowledge_base" - Si pregunta sobre procedimientos bancarios como abrir cuentas, solicitar tarjetas, hacer transferencias, requisitos, pasos, etc.
   Ejemplos: "¿Cómo abro una cuenta?", "Requisitos para tarjeta de crédito", "¿Cómo hago una transferencia?"

3. "general" - Cualquier otra pregunta general, saludos, o temas no relacionados directamente con balance o procedimientos
   Ejemplos: "¿Qué es la inflación?", "Hola", "¿Qué hora es?", "Explícame qué es un interés compuesto"

Consulta del usuario: {query}

Responde ÚNICAMENTE con una de estas palabras: balance, knowledge_base, general

Clasificación:"""
        )
    
    def classify_query(self, query: str) -> Dict[str, any]:
        """
        Clasifica una consulta del usuario.
        
        Args:
            query: Consulta del usuario
        
        Returns:
            Diccionario con el tipo de consulta y confianza
        """
        try:
            # Generar clasificación
            response = self.llm.invoke(
                self.classification_prompt.format(query=query)
            )
            
            # Extraer clasificación del texto de respuesta
            classification = response.content.strip().lower()
            
            # Validar que la clasificación sea válida
            valid_types = ["balance", "knowledge_base", "general"]
            
            # Buscar la clasificación en la respuesta
            query_type = None
            for valid_type in valid_types:
                if valid_type in classification:
                    query_type = valid_type
                    break
            
            if not query_type:
                # Si no se encuentra una clasificación válida, usar general por defecto
                query_type = "general"
            
            return {
                "success": True,
                "query_type": query_type,
                "raw_classification": classification
            }
            
        except Exception as e:
            # En caso de error, clasificar como general
            return {
                "success": False,
                "query_type": "general",
                "error": str(e)
            }
    
    def route_query(self, query: str) -> QueryType:
        """
        Enruta una consulta y retorna el tipo.
        
        Args:
            query: Consulta del usuario
        
        Returns:
            Tipo de consulta (balance, knowledge_base, o general)
        """
        result = self.classify_query(query)
        return result["query_type"]
