"""
Sistema principal de atención al cliente.
Coordina el router y las herramientas para responder consultas.
"""

from typing import Dict
from src.config import Config
from src.agents import QueryRouter
from src.tools import CSVBalanceTool, KnowledgeBaseTool, GeneralLLMTool


class CustomerServiceSystem:
    """Sistema principal de atención al cliente"""
    
    def __init__(self):
        """Inicializa el sistema con todas las herramientas"""
        
        # Validar configuración
        Config.validate()
        
        # Inicializar router
        self.router = QueryRouter(
            api_key=Config.GROQ_API_KEY,
            model=Config.LLM_MODEL
        )
        
        # Inicializar herramientas
        self.csv_tool = CSVBalanceTool(Config.DATA_CSV_PATH)
        
        self.kb_tool = KnowledgeBaseTool(
            kb_path=Config.KNOWLEDGE_BASE_PATH,
            vectorstore_path=Config.VECTORSTORE_PATH,
            embedding_model=Config.EMBEDDING_MODEL
        )
        
        self.llm_tool = GeneralLLMTool(
            api_key=Config.GROQ_API_KEY,
            model=Config.LLM_MODEL
        )
        
        print("✅ Sistema de atención al cliente inicializado correctamente")
    
    def process_query(self, query: str) -> Dict[str, any]:
        """
        Procesa una consulta del usuario.
        
        Args:
            query: Consulta del usuario
        
        Returns:
            Diccionario con la respuesta y metadatos
        """
        
        if not query or not query.strip():
            return {
                "success": False,
                "error": "empty_query",
                "message": "Por favor, ingresa una consulta válida.",
                "query_type": None
            }
        
        try:
            # Clasificar la consulta
            classification = self.router.classify_query(query)
            query_type = classification["query_type"]
            
            # Procesar según el tipo
            if query_type == "balance":
                return self._process_balance_query(query)
            
            elif query_type == "knowledge_base":
                return self._process_kb_query(query)
            
            else:  # general
                return self._process_general_query(query)
        
        except Exception as e:
            return {
                "success": False,
                "error": "system_error",
                "message": "Lo sentimos, el servicio se encuentra temporalmente caído. Por favor, intenta más tarde.",
                "details": str(e)
            }
    
    def _process_balance_query(self, query: str) -> Dict[str, any]:
        """Procesa consultas de balance"""
        try:
            result = self.csv_tool.search_balance(query)
            
            if not result["success"]:
                if result["error"] == "not_found":
                    message = result["message"]
                else:
                    message = "No se pudo resolver la consulta. Por favor, verifica el número de cédula en formato V-XXXXXXXX e intenta nuevamente."
                
                return {
                    "success": False,
                    "query_type": "balance",
                    "message": message,
                    "error": result.get("error")
                }
            
            return {
                "success": True,
                "query_type": "balance",
                "message": result["message"],
                "data": result.get("data")
            }
            
        except Exception as e:
            return {
                "success": False,
                "query_type": "balance",
                "message": "Error al consultar el saldo. Por favor, intenta nuevamente.",
                "error": str(e)
            }
    
    def _process_kb_query(self, query: str) -> Dict[str, any]:
        """Procesa consultas de la base de conocimientos"""
        try:
            # Buscar en la base de conocimientos
            search_result = self.kb_tool.search(query)
            
            if not search_result["success"]:
                return {
                    "success": False,
                    "query_type": "knowledge_base",
                    "message": "No se encontró información relevante sobre tu consulta. Por favor, reformula tu pregunta o contacta a un representante.",
                    "error": search_result.get("error")
                }
            
            # Usar el LLM para generar una respuesta basada en el contexto
            llm_result = self.llm_tool.answer_with_context(
                question=query,
                context=search_result["context"]
            )
            
            if not llm_result["success"]:
                return {
                    "success": False,
                    "query_type": "knowledge_base",
                    "message": "Error al generar la respuesta. Por favor, intenta nuevamente.",
                    "error": llm_result.get("error")
                }
            
            return {
                "success": True,
                "query_type": "knowledge_base",
                "message": llm_result["answer"],
                "sources": search_result.get("sources", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "query_type": "knowledge_base",
                "message": "Error al procesar la consulta. Por favor, intenta nuevamente.",
                "error": str(e)
            }
    
    def _process_general_query(self, query: str) -> Dict[str, any]:
        """Procesa consultas generales"""
        try:
            result = self.llm_tool.answer(query)
            
            if not result["success"]:
                return {
                    "success": False,
                    "query_type": "general",
                    "message": "Lo sentimos, no pudimos procesar tu consulta. Por favor, intenta reformularla.",
                    "error": result.get("error")
                }
            
            return {
                "success": True,
                "query_type": "general",
                "message": result["answer"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "query_type": "general",
                "message": "Error al procesar la consulta general. Por favor, intenta nuevamente.",
                "error": str(e)
            }
    
    def rebuild_knowledge_base(self):
        """Reconstruye la base de conocimientos"""
        self.kb_tool.rebuild_vectorstore()
