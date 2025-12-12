"""
Herramienta para consultar la base de conocimientos usando embeddings y FAISS.
"""

import os
from pathlib import Path
from typing import List, Dict
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader


class KnowledgeBaseTool:
    """Herramienta para consultar la base de conocimientos bancarios"""
    
    def __init__(self, kb_path: Path, vectorstore_path: Path, embedding_model: str):
        """
        Inicializa la herramienta de knowledge base.
        
        Args:
            kb_path: Ruta al directorio con los archivos de conocimiento
            vectorstore_path: Ruta donde guardar/cargar el vectorstore
            embedding_model: Nombre del modelo de embeddings a usar
        """
        self.kb_path = kb_path
        self.vectorstore_path = vectorstore_path
        self.embedding_model = embedding_model
        self.embeddings = None
        self.vectorstore = None
        
        self._initialize()
    
    def _initialize(self):
        """Inicializa los embeddings y el vectorstore"""
        # Crear embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        
        # Cargar o crear vectorstore
        if self._vectorstore_exists():
            self._load_vectorstore()
        else:
            self._create_vectorstore()
    
    def _vectorstore_exists(self) -> bool:
        """Verifica si el vectorstore ya existe"""
        index_file = self.vectorstore_path / "index.faiss"
        return index_file.exists()
    
    def _load_vectorstore(self):
        """Carga el vectorstore existente"""
        try:
            self.vectorstore = FAISS.load_local(
                str(self.vectorstore_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("✅ Vectorstore cargado exitosamente")
        except Exception as e:
            print(f"⚠️  Error al cargar vectorstore: {e}")
            print("🔄 Creando nuevo vectorstore...")
            self._create_vectorstore()
    
    def _create_vectorstore(self):
        """Crea un nuevo vectorstore desde los archivos de conocimiento"""
        try:
            # Cargar documentos
            loader = DirectoryLoader(
                str(self.kb_path),
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            documents = loader.load()
            
            if not documents:
                raise ValueError(f"No se encontraron documentos en {self.kb_path}")
            
            # Dividir documentos en chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                length_function=len
            )
            splits = text_splitter.split_documents(documents)
            
            # Crear vectorstore
            self.vectorstore = FAISS.from_documents(splits, self.embeddings)
            
            # Guardar vectorstore
            self.vectorstore_path.mkdir(parents=True, exist_ok=True)
            self.vectorstore.save_local(str(self.vectorstore_path))
            
            print(f"✅ Vectorstore creado con {len(splits)} chunks y guardado en {self.vectorstore_path}")
            
        except Exception as e:
            raise ValueError(f"Error al crear vectorstore: {e}")
    
    def search(self, query: str, k: int = 3) -> Dict[str, any]:
        """
        Busca en la base de conocimientos.
        
        Args:
            query: Consulta del usuario
            k: Número de documentos relevantes a retornar
        
        Returns:
            Diccionario con los resultados de la búsqueda
        """
        try:
            # Buscar documentos relevantes
            docs = self.vectorstore.similarity_search(query, k=k)
            
            if not docs:
                return {
                    "success": False,
                    "error": "no_results",
                    "message": "No se encontró información relevante en la base de conocimientos."
                }
            
            # Combinar los documentos encontrados
            context = "\n\n".join([doc.page_content for doc in docs])
            
            return {
                "success": True,
                "context": context,
                "num_results": len(docs),
                "sources": [doc.metadata.get('source', 'unknown') for doc in docs]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "search_error",
                "message": f"Error al buscar en la base de conocimientos: {str(e)}"
            }
    
    def rebuild_vectorstore(self):
        """Reconstruye el vectorstore desde cero"""
        print("🔄 Reconstruyendo vectorstore...")
        self._create_vectorstore()
        print("✅ Vectorstore reconstruido exitosamente")
