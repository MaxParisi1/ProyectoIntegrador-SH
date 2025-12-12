"""
Herramienta para consultar saldos de cuentas en el archivo CSV.
"""

import pandas as pd
from typing import Dict, Optional
from pathlib import Path


class CSVBalanceTool:
    """Herramienta para consultar balances de cuentas desde CSV"""
    
    def __init__(self, csv_path: Path):
        """
        Inicializa la herramienta con la ruta al archivo CSV.
        
        Args:
            csv_path: Ruta al archivo CSV con los datos de saldos
        """
        self.csv_path = csv_path
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Carga los datos del CSV"""
        try:
            self.df = pd.read_csv(self.csv_path)
            # Limpiar espacios en blanco de las columnas
            self.df.columns = self.df.columns.str.strip()
            # Limpiar espacios en blanco de la columna ID_Cedula
            if 'ID_Cedula' in self.df.columns:
                self.df['ID_Cedula'] = self.df['ID_Cedula'].astype(str).str.strip()
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo CSV: {e}")
    
    def get_balance(self, cedula: str) -> Dict[str, any]:
        """
        Obtiene el balance de una cuenta dado un ID de cédula.
        
        Args:
            cedula: ID de cédula a buscar (ej: "V-12345678")
        
        Returns:
            Diccionario con la información de la cuenta o error
        """
        # Limpiar la cédula de entrada
        cedula = cedula.strip()
        
        # Buscar en el DataFrame
        result = self.df[self.df['ID_Cedula'] == cedula]
        
        if result.empty:
            return {
                "success": False,
                "error": "not_found",
                "message": f"No se encontró ninguna cuenta asociada a la cédula {cedula}. Por favor, verifica el número de cédula e intenta nuevamente."
            }
        
        # Obtener los datos de la primera coincidencia
        row = result.iloc[0]
        
        return {
            "success": True,
            "data": {
                "cedula": row['ID_Cedula'],
                "nombre": row['Nombre'],
                "balance": float(row['Balance'])
            },
            "message": f"El saldo de la cuenta de {row['Nombre']} (Cédula: {row['ID_Cedula']}) es de ${row['Balance']:.2f}"
        }
    
    def search_balance(self, query: str) -> Dict[str, any]:
        """
        Busca un balance basándose en una consulta en lenguaje natural.
        Intenta extraer el número de cédula de la consulta.
        
        Args:
            query: Consulta en lenguaje natural
        
        Returns:
            Diccionario con la información de la cuenta o error
        """
        import re
        
        # Buscar patrón de cédula (V-XXXXXXXX o similar)
        pattern = r'[VEJGvejg]-?\d{7,8}'
        matches = re.findall(pattern, query)
        
        if not matches:
            return {
                "success": False,
                "error": "no_cedula_found",
                "message": "No se pudo identificar un número de cédula en la consulta. Por favor, proporciona la cédula en formato V-XXXXXXXX."
            }
        
        # Normalizar la cédula (agregar guion si no lo tiene)
        cedula = matches[0].upper()
        if '-' not in cedula and len(cedula) > 1:
            cedula = cedula[0] + '-' + cedula[1:]
        
        return self.get_balance(cedula)
    
    def get_all_balances(self) -> pd.DataFrame:
        """
        Retorna todos los balances disponibles.
        
        Returns:
            DataFrame con todos los datos
        """
        return self.df.copy()
