# Sistema de Atención al Cliente - BANCO HENRY

## Documentación Técnica Detallada

### Descripción General

Sistema automatizado de atención al cliente desarrollado con LangChain que procesa solicitudes de usuarios y decide inteligentemente el método más apropiado para responder. El sistema integra tres flujos principales:

1. **Consulta de balances**: Búsqueda en CSV de saldos por número de cédula
2. **Base de conocimientos**: Recuperación de información bancaria usando FAISS y embeddings
3. **Respuestas generales**: Generación de respuestas usando LLM (Groq) para temas financieros

---

## 1. Instrucciones de Instalación y Ejecución

### Requisitos Previos

- **Python 3.10 o superior** (desarrollado y testeado en Python 3.14)
- **Cuenta de Groq** con API Key activa (obtener en https://console.groq.com/)
- **Sistema operativo**: macOS, Linux, o Windows con WSL

### Instalación Paso a Paso

#### Opción 1: Instalación con Makefile (Recomendada)

```bash
# 1. Ubicarse en el directorio del proyecto
cd /ruta/a/proyecto

# 2. Instalar dependencias y crear entorno virtual
make setup

# 3. Configurar API Key de Groq
cp .env.example .env
# Editar .env y agregar: GROQ_API_KEY=tu_api_key_aqui

# 4. Ejecutar la aplicación
make run
```

#### Opción 2: Instalación Manual

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar GROQ_API_KEY

# 4. Ejecutar aplicación
streamlit run app.py
```

### Comandos Disponibles

El proyecto incluye un Makefile simplificado con comandos esenciales:

```bash
make setup     # Crear venv e instalar todas las dependencias
make run       # Iniciar la aplicación Streamlit
make test      # Ejecutar tests unitarios con pytest
make validate  # Ejecutar validación con 10 consultas de prueba
make clean     # Limpiar archivos temporales y caché
```

### Verificación de Instalación

Para verificar que todo está instalado correctamente:

```bash
# Ejecutar tests unitarios
make test

# Ejecutar validación (requiere GROQ_API_KEY configurada)
make validate
```

---

## 2. Arquitectura del Sistema y Decisiones de Diseño

### Arquitectura General

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Router Agent (LLM Classifier)   │
│  Analiza consulta y determina tipo  │
└──────────┬──────────────────────────┘
           │
           ├─────────┬─────────|
           ▼         ▼         ▼          
      ┌────────┐ ┌────────┐ ┌────────┐
      │ CSV    │ │ KB     │ │ LLM    │
      │ Tool   │ │ Tool   │ │ Tool   │
      └────┬───┘ └───┬────┘ └───┬────┘
           │         │          │
           └────┬────┴────┬─────┘
                │         │
                ▼         ▼
          ┌──────────────────┐
          │    Respuesta     │
          └──────────────────┘
```

### Componentes Principales

#### 1. Router Agent (`src/agents/router.py`)

**Decisión de diseño**: Usar un enfoque de routing con LLM en lugar de un agente autónomo.

**Razones**:
- **Simplicidad**: El routing es más predecible y fácil de debuggear que un agente complejo
- **Control**: Tenemos control total sobre qué herramienta se usa en cada caso
- **Performance**: Evitamos múltiples llamadas al LLM (el agente autónomo requeriría reasoning adicional)
- **Costos**: Una sola llamada al LLM para clasificar vs múltiples llamadas para decidir

El router analiza la consulta del usuario y devuelve uno de tres tipos:
- `balance`: Para consultas sobre saldos de cuenta
- `knowledge_base`: Para preguntas sobre procesos bancarios
- `general`: Para consultas financieras generales

#### 2. LLM Tool (`src/tools/llm_tool.py`)

**Decisión de diseño**: Usar Groq con `llama-3.3-70b-versatile` y system prompt restrictivo.

- **System prompt**: Limitamos respuestas solo a temas financieros

**Funcionalidad**:
- Responde preguntas financieras generales
- Rechaza cortésmente preguntas fuera de alcance
- Mantiene contexto bancario en las respuestas

### Estructura Modular

```
src/
├── main.py                  # Orquestador principal (CustomerServiceSystem)
├── config/
│   └── settings.py          # Configuración centralizada (GROQ_API_KEY, paths)
├── agents/
│   └── router.py            # Router LLM para clasificación
└── tools/
    ├── csv_tool.py          # Herramienta de consulta CSV
    ├── kb_tool.py           # Herramienta de knowledge base
    └── llm_tool.py          # Herramienta de LLM general
```

**Decisión de diseño**: Arquitectura modular con separación de responsabilidades.

**Beneficios**:
- **Testabilidad**: Cada componente puede testearse independientemente
- **Mantenibilidad**: Cambios en una herramienta no afectan las otras
- **Extensibilidad**: Fácil agregar nuevas herramientas o modificar el router

### Manejo de Errores

El sistema implementa manejo robusto de errores en cada capa:

1. **Router**: Si falla la clasificación, usa categoría "general" como fallback
2. **CSV Tool**: Retorna mensaje claro si el cliente no existe
3. **KB Tool**: Maneja casos donde no hay documentos relevantes
4. **LLM Tool**: Captura errores de API y retorna mensajes informativos

---

## 3. Ejemplos de Uso con Casos de Prueba

### Script de Validación

El proyecto incluye un script de validación con 10 consultas de prueba que cubren los tres flujos:

```bash
make validate
```

**Consultas incluidas**:

#### Consultas de Balance (3 casos)

1. **Caso básico**:
   - Consulta: "¿Cuál es el balance de la cuenta del cliente con cédula 12345678?"
   - Tipo esperado: `balance`
   - Respuesta esperada: Saldo de cuenta corriente y ahorros del cliente 12345678

2. **Caso con formato diferente**:
   - Consulta: "Quiero saber cuánto dinero tiene el cliente 87654321"
   - Tipo esperado: `balance`
   - Respuesta esperada: Información de saldos del cliente 87654321

3. **Caso con cliente inexistente**:
   - Consulta: "Balance de la cédula 99999999"
   - Tipo esperado: `balance`
   - Respuesta esperada: Mensaje indicando que el cliente no existe

#### Consultas de Knowledge Base (4 casos)

4. **Caso de apertura de cuenta**:
   - Consulta: "¿Cómo puedo abrir una cuenta nueva?"
   - Tipo esperado: `knowledge_base`
   - Respuesta esperada: Procedimiento para abrir cuenta desde `nueva_cuenta.txt`

5. **Caso de transferencias**:
   - Consulta: "¿Cuáles son los pasos para hacer una transferencia?"
   - Tipo esperado: `knowledge_base`
   - Respuesta esperada: Procedimiento de transferencias desde `transferencia.txt`

6. **Caso de tarjeta de crédito**:
   - Consulta: "Quiero solicitar una tarjeta de crédito"
   - Tipo esperado: `knowledge_base`
   - Respuesta esperada: Requisitos y proceso desde `tarjeta_credito.txt`

7. **Caso de límites de transferencia**:
   - Consulta: "¿Cuál es el límite máximo para transferencias?"
   - Tipo esperado: `knowledge_base`
   - Respuesta esperada: Información de límites desde base de conocimientos

#### Consultas Generales (3 casos)

8. **Caso de tasa de interés**:
   - Consulta: "¿Qué es una tasa de interés?"
   - Tipo esperado: `general`
   - Respuesta esperada: Explicación general sobre tasas de interés

9. **Caso de inflación**:
   - Consulta: "¿Cómo afecta la inflación a mis ahorros?"
   - Tipo esperado: `general`
   - Respuesta esperada: Explicación sobre inflación y ahorros

10. **Caso de inversión**:
    - Consulta: "¿Qué diferencia hay entre ahorro e inversión?"
    - Tipo esperado: `general`
    - Respuesta esperada: Comparación entre ahorro e inversión

### Ejemplo de Salida de Validación

```
Ejecutando validación con 10 consultas de prueba...
================================================

Consulta 1/10
Pregunta: ¿Cuál es el balance de la cuenta del cliente con cédula 12345678?
Tipo detectado: balance
Respuesta: El cliente con cédula 12345678 tiene un saldo de $5,432.10 en cuenta corriente...

Consulta 2/10
Pregunta: Quiero saber cuánto dinero tiene el cliente 87654321
Tipo detectado: balance
Respuesta: El cliente con cédula 87654321 tiene $12,890.50 en cuenta corriente...

[... más consultas ...]

Consulta 10/10
Pregunta: ¿Qué diferencia hay entre ahorro e inversión?
Tipo detectado: general
Respuesta: El ahorro consiste en guardar dinero sin riesgo, mientras que la inversión...

================================================
Validación completada: 10/10 consultas procesadas exitosamente
```

### Uso en la Interfaz Streamlit

Al ejecutar `make run`, se abre una interfaz web donde puedes:

1. **Hacer consultas**: Escribir en el chat cualquier pregunta
2. **Ver el tipo detectado**: El sistema muestra si es balance, KB, o general
3. **Reconstruir KB**: Botón para regenerar el índice FAISS si modificas documentos
4. **Ver ejemplos**: Sección con consultas de ejemplo para cada tipo

---

## 4. Dependencias y Requisitos del Sistema

### Dependencias de Python

**Core LangChain**:
```
langchain==0.3.20
langchain-core==0.3.30
langchain-community==0.3.20
langchain-text-splitters==0.3.4
```

**Groq Integration**:
```
langchain-groq==0.3.2
groq==0.13.0
```

**Embeddings y Vector Store**:
```
langchain-huggingface==0.1.2
sentence-transformers==3.4.1
faiss-cpu==1.9.0.post1
```

**UI y Utilidades**:
```
streamlit==1.42.0
pandas==2.2.3
python-dotenv==1.0.1
```

**Testing**:
```
pytest==8.3.4
```

### Requisitos del Sistema

**Software**:
- Python 3.10, 3.11, 3.12, 3.13, o 3.14
- pip (incluido con Python)
- venv (incluido con Python)

### Variables de Entorno Requeridas

Crear archivo `.env` en la raíz con:

```bash
# REQUERIDO: API Key de Groq
GROQ_API_KEY=gsk_tu_api_key_aqui

# OPCIONAL: Modelo de Groq a usar (default: llama-3.3-70b-versatile)
GROQ_MODEL=llama-3.3-70b-versatile

# OPCIONAL: HuggingFace token (solo si usas modelos gated)
HUGGINGFACE_TOKEN=hf_tu_token_aqui
```

### Obtener API Keys

**Groq API Key** (REQUERIDA):
1. Ir a https://console.groq.com/
2. Crear cuenta gratuita
3. Navegar a API Keys
4. Crear nueva key
5. Copiar y pegar en `.env`

**HuggingFace Token** (OPCIONAL):
1. Ir a https://huggingface.co/
2. Crear cuenta
3. Settings → Access Tokens
4. Create new token (read)
5. Copiar y pegar en `.env`

---

## Validación y Entrega

### Cómo Ejecutar Validación Completa

```bash
# 1. Setup inicial
make setup

# 2. Configurar .env
cp .env.example .env
# Editar y agregar GROQ_API_KEY

# 3. Ejecutar tests unitarios
make test

# 4. Ejecutar validación de 10 consultas
make validate

# 5. Ejecutar aplicación
make run
```

---

## Estructura del Proyecto

```
.
├── README.md                        # Este archivo
├── .env.example                     # Template de variables de entorno
├── .env                             # Variables de entorno (no en git)
├── requirements.txt                 # Dependencias Python
├── Makefile                         # Comandos automatizados
│
├── app.py                           # Interfaz Streamlit
│
├── src/                             # Código fuente principal
│   ├── main.py                      # Orquestador CustomerServiceSystem
│   ├── config/
│   │   └── settings.py              # Configuración centralizada
│   ├── agents/
│   │   └── router.py                # Router LLM para clasificación
│   └── tools/
│       ├── csv_tool.py              # Herramienta de consulta CSV
│       ├── kb_tool.py               # Herramienta de knowledge base
│       └── llm_tool.py              # Herramienta de LLM general
│
├── tests/                           # Tests unitarios
│   └── test_system.py               # Suite principal de tests
│
├── scripts/                         # Scripts auxiliares
│   ├── install.sh                   # Script de instalación
│   ├── run.sh                       # Script de ejecución
│   ├── test.sh                      # Script de testing
│   └── run_validation.py            # Script de validación (10 consultas)
│
├── data/                            # Datos CSV
│   └── saldos.csv                   # Saldos de clientes
│
├── knowledge_base/                  # Documentos de KB
│   ├── nueva_cuenta.txt             # Procedimiento apertura de cuenta
│   ├── tarjeta_credito.txt          # Procedimiento tarjeta de crédito
│   └── transferencia.txt            # Procedimiento transferencias
│
└── vectorstore/                     # Índice FAISS persistente
    └── index.faiss                  # (generado automáticamente)
```
