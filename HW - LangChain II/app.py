"""
Interfaz gráfica con Streamlit para el sistema de atención al cliente.
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from src.main import CustomerServiceSystem
from src.config import Config


# Configuración de la página
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1E88E5;
        margin-bottom: 2rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #FFEBEE;
        border-left: 4px solid #F44336;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        border-radius: 4px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_system():
    """Inicializa el sistema si no está en session_state"""
    if 'system' not in st.session_state:
        with st.spinner("🔄 Inicializando sistema..."):
            try:
                st.session_state.system = CustomerServiceSystem()
                st.session_state.initialized = True
                st.session_state.chat_history = []
            except Exception as e:
                st.error(f"❌ Error al inicializar el sistema: {str(e)}")
                st.session_state.initialized = False


def display_chat_message(role: str, content: str, query_type: str = None):
    """Muestra un mensaje en el chat"""
    with st.chat_message(role):
        st.markdown(content)
        if role == "assistant" and query_type:
            # Mostrar badge del tipo de consulta
            type_labels = {
                "balance": "💰 Consulta de Saldo",
                "knowledge_base": "📚 Base de Conocimientos",
                "general": "💬 Consulta General"
            }
            if query_type in type_labels:
                st.caption(f"*{type_labels[query_type]}*")


def main():
    """Función principal de la aplicación"""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 BANCO HENRY - Asistente Virtual</h1>', unsafe_allow_html=True)
    
    # Inicializar sistema
    initialize_system()
    
    # Sidebar con información
    with st.sidebar:
        st.header("ℹ️ Información del Sistema")
        
        st.markdown("""
        ### ¿Qué puedo hacer?
        
        **💰 Consultar Saldos**
        - Pregunta por tu saldo
        - Usa tu número de cédula
        - Ejemplo: *"¿Cuál es el saldo de V-12345678?"*
        
        **📚 Procedimientos Bancarios**
        - Cómo abrir una cuenta
        - Solicitar tarjeta de crédito
        - Realizar transferencias
        
        **💬 Preguntas Generales**
        - Conceptos financieros
        - Información general
        - Cualquier otra consulta
        """)
        
        st.divider()
        
        # Estadísticas de la sesión
        if 'chat_history' in st.session_state:
            st.metric("Consultas Realizadas", len(st.session_state.chat_history))
        
        st.divider()
        
        # Botón para limpiar chat
        if st.button("🗑️ Limpiar Historial", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        # Botón para reconstruir knowledge base
        if st.button("🔄 Reconstruir Base de Conocimientos", use_container_width=True):
            with st.spinner("Reconstruyendo..."):
                st.session_state.system.rebuild_knowledge_base()
                st.success("✅ Base de conocimientos reconstruida")
    
    # Verificar que el sistema esté inicializado
    if not st.session_state.get('initialized', False):
        st.error("❌ El sistema no pudo ser inicializado. Verifica la configuración.")
        return
    
    # Ejemplos de consultas
    with st.expander("💡 Ver ejemplos de consultas"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**💰 Consultas de Saldo**")
            st.code("¿Cuál es el saldo de V-12345678?")
            st.code("Saldo de la cédula V-87654321")
            st.code("¿Cuánto dinero tiene Juan Pérez?")
        
        with col2:
            st.markdown("**📚 Procedimientos**")
            st.code("¿Cómo abro una cuenta?")
            st.code("Requisitos para tarjeta de crédito")
            st.code("¿Cómo hago una transferencia internacional?")
        
        with col3:
            st.markdown("**💬 Generales**")
            st.code("¿Qué es la inflación?")
            st.code("Explícame qué es un interés compuesto")
            st.code("¿Cuál es la diferencia entre débito y crédito?")
    
    st.divider()
    
    # Mostrar historial de chat
    for message in st.session_state.chat_history:
        display_chat_message(
            message["role"],
            message["content"],
            message.get("query_type")
        )
    
    # Input del usuario
    if prompt := st.chat_input("💬 Escribe tu consulta aquí..."):
        
        # Mostrar mensaje del usuario
        display_chat_message("user", prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Procesar consulta
        with st.spinner("🤔 Procesando tu consulta..."):
            try:
                response = st.session_state.system.process_query(prompt)
                
                # Mostrar respuesta
                if response["success"]:
                    display_chat_message(
                        "assistant",
                        response["message"],
                        response.get("query_type")
                    )
                    
                    # Guardar en historial
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response["message"],
                        "query_type": response.get("query_type")
                    })
                    
                    # Mostrar datos adicionales si existen
                    if "data" in response and response["data"]:
                        with st.expander("📊 Ver detalles"):
                            st.json(response["data"])
                    
                    if "sources" in response and response["sources"]:
                        with st.expander("📑 Fuentes consultadas"):
                            for source in response["sources"]:
                                st.text(f"• {Path(source).name}")
                
                else:
                    error_msg = response.get("message", "Error desconocido")
                    display_chat_message("assistant", f"❌ {error_msg}")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"❌ {error_msg}",
                        "query_type": response.get("query_type")
                    })
            
            except Exception as e:
                error_msg = "Lo sentimos, el servicio se encuentra temporalmente caído. Por favor, intenta más tarde."
                display_chat_message("assistant", f"❌ {error_msg}")
                st.error(f"Error técnico: {str(e)}")
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"❌ {error_msg}"
                })


if __name__ == "__main__":
    main()
