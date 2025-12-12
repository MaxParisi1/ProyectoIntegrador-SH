"""
Herramienta para responder consultas generales usando el LLM.
"""

from typing import Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


class GeneralLLMTool:
    """Herramienta para responder preguntas generales con el LLM"""
    
    def __init__(self, api_key: str, model: str):
        """
        Inicializa la herramienta de LLM.
        
        Args:
            api_key: API key de Groq
            model: Nombre del modelo a usar
        """
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=0.3
        )
        
        # Template para respuestas generales
        self.prompt_template = PromptTemplate(
            input_variables=["question"],
            template="""Eres un asistente virtual del BANCO HENRY, especializado en temas bancarios y financieros.

IMPORTANTE: Solo puedes responder preguntas relacionadas con:
- Servicios bancarios (cuentas, tarjetas, transferencias, préstamos)
- Conceptos financieros (inflación, tasas de interés, ahorro, inversión)
- Economía y finanzas personales

Si la pregunta NO está relacionada con estos temas (por ejemplo: videojuegos, deportes, entretenimiento, tecnología general, etc.), debes responder amablemente:
"Lo siento, soy un asistente especializado en servicios bancarios y financieros del BANCO HENRY. Solo puedo ayudarte con consultas relacionadas con servicios bancarios, finanzas personales y conceptos económicos. ¿Hay algo sobre estos temas en lo que pueda ayudarte?"

Pregunta: {question}

Respuesta:"""
        )
        
        # Crear chain usando pipe operator (nuevo API)
        self.chain = self.prompt_template | self.llm
    
    def answer(self, question: str) -> Dict[str, any]:
        """
        Responde una pregunta general usando el LLM.
        
        Args:
            question: Pregunta del usuario
        
        Returns:
            Diccionario con la respuesta
        """
        try:
            response = self.chain.invoke({"question": question})
            
            return {
                "success": True,
                "answer": response.content.strip(),
                "source": "llm"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "llm_error",
                "message": f"Error al generar respuesta: {str(e)}"
            }
    
    def answer_with_context(self, question: str, context: str) -> Dict[str, any]:
        """
        Responde una pregunta usando contexto adicional.
        
        Args:
            question: Pregunta del usuario
            context: Contexto adicional para responder
        
        Returns:
            Diccionario con la respuesta
        """
        try:
            context_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""Eres un asistente del BANCO HENRY. Usa la siguiente información para responder la pregunta del cliente.

Información disponible:
{context}

Pregunta del cliente: {question}

Proporciona una respuesta clara, precisa y profesional basada en la información proporcionada.

Respuesta:"""
            )
            
            context_chain = context_prompt | self.llm
            response = context_chain.invoke({"context": context, "question": question})
            
            return {
                "success": True,
                "answer": response.content.strip(),
                "source": "llm_with_context"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "llm_error",
                "message": f"Error al generar respuesta con contexto: {str(e)}"
            }
