# Guía Completa de Mejores Prácticas para Unit Testing con pytest

## 1. Estructura y Organización

### 1.1 Estructura de Directorios
```
project/
├── src/
│   └── module.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_module.py       # Tests para module.py
│   └── integration/         # Tests de integración
└── pytest.ini               # Configuración pytest
```

### 1.2 Convenciones de Nombres
- **Archivos**: `test_*.py` o `*_test.py`
- **Funciones**: `test_descripcion_clara()`
- **Clases**: `TestNombreDelModulo` o `TestFuncionalidad`
- **Fixtures**: nombres descriptivos en minúsculas con guiones bajos

---

## 2. Principios Fundamentales

### 2.1 FIRST Principles
- **Fast**: Tests rápidos (< 1 segundo idealmente)
- **Independent**: Tests aislados e independientes
- **Repeatable**: Resultados consistentes en cualquier ambiente
- **Self-Validating**: Pass/fail sin interpretación manual
- **Timely**: Escribir tests junto con el código

### 2.2 Patrón AAA (Arrange-Act-Assert)
```python
def test_example():
    # Arrange: Preparar datos y estado inicial
    initial_value = 100
    rate = 0.05
    
    # Act: Ejecutar la función bajo prueba
    result = calculate_interest(initial_value, rate)
    
    # Assert: Verificar el resultado esperado
    assert result == 105.0
```

### 2.3 Given-When-Then (BDD Style)
```python
def test_user_login():
    """
    Given: Un usuario registrado con credenciales válidas
    When: El usuario intenta iniciar sesión
    Then: El sistema autentica exitosamente
    """
    # Given
    user = create_user("test@example.com", "password123")
    
    # When
    result = authenticate(user.email, "password123")
    
    # Then
    assert result.is_authenticated is True
```

---

## 3. Parametrización con pytest

### 3.1 Parametrización Básica
```python
@pytest.mark.parametrize(
    "input_value, expected",
    [
        (1, 2),
        (2, 4),
        (3, 6),
    ],
    ids=["caso_uno", "caso_dos", "caso_tres"]
)
def test_double(input_value, expected):
    assert double(input_value) == expected
```

### 3.2 Parametrización Múltiple
```python
@pytest.mark.parametrize("principal", [1000, 5000, 10000])
@pytest.mark.parametrize("rate", [0.05, 0.10, 0.15])
def test_combinations(principal, rate):
    result = calculate_interest(principal, rate)
    assert result > principal
```

### 3.3 Parametrización con Diccionarios
```python
@pytest.mark.parametrize(
    "params",
    [
        {"principal": 1000, "rate": 0.05, "periods": 1, "expected": 1050},
        {"principal": 2000, "rate": 0.10, "periods": 2, "expected": 2420},
    ]
)
def test_with_dict(params):
    result = calculate_compound_interest(
        params["principal"], 
        params["rate"], 
        params["periods"]
    )
    assert result == pytest.approx(params["expected"])
```

---

## 4. Fixtures en pytest

### 4.1 Fixtures Básicas
```python
@pytest.fixture
def sample_data():
    """Fixture que retorna datos de prueba."""
    return {"name": "Test", "value": 100}

def test_with_fixture(sample_data):
    assert sample_data["value"] == 100
```

### 4.2 Fixtures con Setup/Teardown
```python
@pytest.fixture
def database_connection():
    # Setup
    conn = create_database_connection()
    yield conn  # Provee la conexión al test
    # Teardown
    conn.close()

def test_database(database_connection):
    result = database_connection.query("SELECT 1")
    assert result is not None
```

### 4.3 Scopes de Fixtures
```python
@pytest.fixture(scope="function")  # Default: cada test
def function_scope():
    return setup_resource()

@pytest.fixture(scope="class")  # Una vez por clase
def class_scope():
    return setup_expensive_resource()

@pytest.fixture(scope="module")  # Una vez por módulo
def module_scope():
    return setup_very_expensive_resource()

@pytest.fixture(scope="session")  # Una vez por sesión
def session_scope():
    return setup_database()
```

### 4.4 Fixtures Parametrizadas
```python
@pytest.fixture(params=[0.05, 0.10, 0.15])
def interest_rate(request):
    return request.param

def test_various_rates(interest_rate):
    result = calculate_interest(1000, interest_rate)
    assert result > 1000
```

### 4.5 conftest.py - Fixtures Compartidas
```python
# conftest.py
import pytest

@pytest.fixture
def shared_resource():
    """Disponible para todos los tests del proyecto."""
    return create_shared_resource()
```

---

## 5. Assertions y Comparaciones

### 5.1 Assertions Básicas
```python
assert valor == esperado
assert valor != no_esperado
assert valor > minimo
assert valor in lista
assert isinstance(objeto, Clase)
assert callable(funcion)
```

### 5.2 Comparación de Flotantes
```python
# ❌ INCORRECTO
assert 0.1 + 0.2 == 0.3  # Puede fallar por precisión

# ✅ CORRECTO
assert 0.1 + 0.2 == pytest.approx(0.3)
assert resultado == pytest.approx(esperado, rel=1e-9)  # Tolerancia relativa
assert resultado == pytest.approx(esperado, abs=0.01)  # Tolerancia absoluta
```

### 5.3 Verificación de Excepciones
```python
def test_exception():
    with pytest.raises(ValueError):
        divide(10, 0)
    
    # Con mensaje específico
    with pytest.raises(ValueError, match="cannot divide by zero"):
        divide(10, 0)
    
    # Capturar para validar atributos
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "zero" in str(exc_info.value)
```

### 5.4 Warnings
```python
def test_warning():
    with pytest.warns(DeprecationWarning):
        legacy_function()
```

---

## 6. Cobertura de Casos

### 6.1 Happy Path (Casos Normales)
```python
def test_normal_case():
    """Test con valores típicos y esperados."""
    result = calculate_compound_interest(1000, 0.05, 5)
    assert result == pytest.approx(1276.28)
```

### 6.2 Edge Cases (Casos Límite)
```python
def test_edge_cases():
    """Test con valores en los límites."""
    assert calculate_interest(0, 0.05) == 0        # Principal cero
    assert calculate_interest(1000, 0) == 1000     # Tasa cero
    assert calculate_interest(1000, 0.05, 0) == 1000  # Períodos cero
    assert calculate_interest(1, 0.01, 1) > 0     # Valores mínimos
```

### 6.3 Corner Cases (Casos Esquina)
```python
def test_corner_cases():
    """Test con combinaciones extremas."""
    assert calculate_interest(0, 0, 0) == 0
    assert calculate_interest(float('inf'), 0.05, 1) == float('inf')
```

### 6.4 Negative Cases (Casos Negativos)
```python
def test_negative_values():
    """Test con valores negativos."""
    result = calculate_interest(-1000, 0.05)
    assert result < 0
    
    result = calculate_interest(1000, -0.05)
    assert result < 1000
```

### 6.5 Boundary Testing (Pruebas de Frontera)
```python
@pytest.mark.parametrize(
    "value",
    [
        -1,    # Justo debajo del límite
        0,     # En el límite inferior
        1,     # Justo arriba del límite
        999,   # Justo debajo del límite superior
        1000,  # En el límite superior
        1001,  # Justo arriba del límite superior
    ]
)
def test_boundaries(value):
    result = validate_range(value, 0, 1000)
    assert isinstance(result, bool)
```

---

## 7. Marks y Metadata

### 7.1 Skip y Skipif
```python
@pytest.mark.skip(reason="Funcionalidad no implementada")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="No corre en Windows")
def test_unix_only():
    pass
```

### 7.2 XFail (Expected to Fail)
```python
@pytest.mark.xfail(reason="Bug conocido #123")
def test_known_bug():
    assert broken_function() == expected
```

### 7.3 Marks Personalizados
```python
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

# En tests
@pytest.mark.slow
def test_expensive_operation():
    pass

@pytest.mark.integration
def test_api_integration():
    pass

# Ejecutar: pytest -m "not slow"
```

---

## 8. Organización de Tests

### 8.1 Clases de Test
```python
class TestCalculator:
    """Agrupa tests relacionados."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup automático para todos los tests de la clase."""
        self.calculator = Calculator()
    
    def test_add(self):
        assert self.calculator.add(2, 3) == 5
    
    def test_subtract(self):
        assert self.calculator.subtract(5, 3) == 2
```

### 8.2 Tests Anidados
```python
class TestUserAuthentication:
    """Tests de autenticación de usuario."""
    
    class TestLogin:
        """Tests específicos de login."""
        
        def test_successful_login(self):
            pass
        
        def test_failed_login(self):
            pass
    
    class TestLogout:
        """Tests específicos de logout."""
        
        def test_successful_logout(self):
            pass
```

---

## 9. Mocking y Patching

### 9.1 Usando pytest-mock
```python
def test_with_mock(mocker):
    # Mock de una función
    mock_api = mocker.patch('module.api_call')
    mock_api.return_value = {"status": "success"}
    
    result = function_that_calls_api()
    assert result["status"] == "success"
    mock_api.assert_called_once()
```

### 9.2 Mock de Side Effects
```python
def test_retry_logic(mocker):
    mock_api = mocker.patch('module.api_call')
    mock_api.side_effect = [
        Exception("Network error"),  # Primera llamada falla
        {"status": "success"}        # Segunda llamada exitosa
    ]
    
    result = function_with_retry()
    assert result["status"] == "success"
    assert mock_api.call_count == 2
```

---

## 10. Documentación de Tests

### 10.1 Docstrings Descriptivos
```python
def test_compound_interest_with_zero_rate():
    """
    Test que verifica el comportamiento cuando la tasa de interés es cero.
    
    Escenario:
        - Principal: $1000
        - Tasa: 0% (sin interés)
        - Períodos: 5
    
    Resultado esperado:
        - El valor futuro debe ser igual al principal inicial
        - No debe haber crecimiento del capital
    """
    result = calculate_compound_interest(1000, 0.0, 5)
    assert result == 1000.0
```

### 10.2 IDs Descriptivos en Parametrización
```python
@pytest.mark.parametrize(
    "principal, rate, periods, expected",
    [
        (1000, 0.05, 1, 1050.0),
        (1000, 0.05, 5, 1276.28),
    ],
    ids=[
        "single_period_5_percent",
        "five_periods_5_percent",
    ]
)
def test_scenarios(principal, rate, periods, expected):
    pass
```

---

## 11. Performance y Optimización

### 11.1 Tests Rápidos
```python
# ✅ BUENO: Test rápido y aislado
def test_calculation():
    assert add(2, 3) == 5

# ❌ MALO: Test lento con dependencias externas
def test_slow():
    time.sleep(5)  # Evitar
    response = requests.get("http://api.com")  # Usar mocks
```

### 11.2 Paralelización
```bash
# Instalar: pip install pytest-xdist
# Ejecutar: pytest -n auto  # Usa todos los cores
```

---

## 12. Configuración pytest.ini

```ini
[pytest]
# Opciones de línea de comando por defecto
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=term-missing

# Directorios a testear
testpaths = tests

# Patrón de archivos de test
python_files = test_*.py *_test.py

# Patrón de clases de test
python_classes = Test*

# Patrón de funciones de test
python_functions = test_*

# Marks personalizados
markers =
    slow: marca tests lentos
    integration: tests de integración
    unit: tests unitarios
    smoke: tests de smoke

# Opciones de cobertura
[coverage:run]
source = src
omit = 
    */tests/*
    */venv/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## 13. Checklist de Calidad

### ✅ Antes de Commitear Tests

- [ ] Nombres descriptivos y claros
- [ ] Documentación con docstrings
- [ ] Patrón AAA respetado
- [ ] Tests independientes (no dependen de orden)
- [ ] Fixtures utilizadas apropiadamente
- [ ] Parametrización para múltiples casos
- [ ] Edge cases cubiertos
- [ ] Assertions precisos (pytest.approx para floats)
- [ ] Excepciones testeadas cuando aplique
- [ ] Tests rápidos (< 1 segundo)
- [ ] Sin código duplicado (usar fixtures)
- [ ] Cobertura > 80%

---

## 14. Comandos Útiles

```bash
# Ejecutar todos los tests
pytest

# Con verbosidad
pytest -v

# Con cobertura
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/test_finance.py
pytest tests/test_finance.py::TestClass::test_method

# Por marks
pytest -m "not slow"
pytest -m "unit and not integration"

# Paralelo
pytest -n auto

# Detener en primer fallo
pytest -x

# Mostrar prints
pytest -s

# Re-ejecutar solo tests fallidos
pytest --lf

# Tests que fallaron y los siguientes
pytest --ff
```

---

## 15. Anti-patrones a Evitar

❌ `assert result == 1276.2815625` (comparación directa de floats)
✅ `assert result == pytest.approx(1276.2815625, rel=1e-9)`

❌ Tests sin documentación
✅ Docstrings descriptivos en cada test

❌ Valores mágicos sin contexto
✅ IDs descriptivos y comentarios explicativos

❌ Tests dependientes entre sí
✅ Tests completamente aislados e independientes

❌ Tests lentos sin mark @pytest.mark.slow
✅ Marcar apropiadamente tests que tardan > 1s

❌ Mock innecesarios
✅ Mock solo dependencias externas (APIs, DB, filesystem)

---
