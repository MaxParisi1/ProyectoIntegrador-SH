# Testing con GitHub Copilot - Proyecto Finance

## Descripción

Desarrollo de una suite de tests unitarios para el módulo `finance.py` usando TDD con pytest. El módulo implementa 3 funciones de cálculos financieros: interés compuesto, anualidades, y TIR.

**Resultado:** 91 tests, 98% cobertura de código.

---

## El Proceso

### 1. Documentación Primero (Modo Ask + Agente)

Antes de escribir un solo test, usé modo Ask para debatir y definir las mejores prácticas de pytest. Después creé dos archivos de documentación:

- **`.github/copilot-instructions.md`**: Guía completa de pytest (15 secciones) con patrones, fixtures, parametrización, assertions.
- **`.github/prompts/pytest-tests.prompt.md`**: Template de 6 fases para aplicar TDD de forma sistemática.

Invertir tiempo en estos archivos ahorró ~70% del tiempo en las siguientes funciones. Son reutilizables para cualquier proyecto Python.

### 2. TDD: RED-GREEN-REFACTOR

Apliqué el mismo proceso para cada función:

**RED (Tests que fallan):**
1. Modo Ask: Análisis de dominio financiero
   - ¿Principal negativo es válido? (SÍ para compound interest, NO para annuity)
   - ¿Rate = -1 es válido? (NO, causa división por cero)
   - ¿TIR con todos flujos positivos? (NO, causa overflow)

2. Modo Agente: Crear 25+ tests en 6 categorías (Happy Path, Edge Cases, Corner Cases, Negative Cases, Boundaries, Mathematical Properties)

3. Ejecutar → ver ~15-20 tests fallar

**GREEN (Hacer pasar tests):**
- Refactorizar función agregando validaciones de tipo, rango, casos especiales
- Ejecutar → 91/91 tests pasan

**REFACTOR:**
- Organizar en clases, usar fixtures, parametrizar, usar `pytest.approx()`

---

## Resultados

```
===================== 91 passed in 0.60s ======================

Name         Stmts   Miss  Cover   Missing
------------------------------------------
finance.py      55      1    98%   280
```

| Función | Tests | Cobertura |
|---------|-------|-----------|
| `calculate_compound_interest` | 29 | 100% |
| `calculate_annuity_payment` | 31 | 100% |
| `calculate_internal_rate_of_return` | 31 | ~96% |

La línea sin cubrir es un `break` en caso extremo de derivada cero en Newton-Raphson (escenario rarísimo en la práctica).

---

## Aprendizajes

**1. Crear documentación reutilizable es la mejor inversión**

Los archivos `.github/copilot-instructions.md` y `pytest-tests.prompt.md` son activos permanentes. Me ahorrarán días en futuros proyectos.

**2. TDD cambia cómo piensas el código**

Antes: función primero, tests después.  
Ahora: pensar casos → escribir tests → implementar. Los tests RED forzaron validaciones que no hubiera considerado.

**3. El análisis de dominio es crítico**

15 minutos en modo Ask debatiendo el dominio evitan horas de refactorización. No puedes testear bien sin entender qué es válido y qué no.

**4. pytest > unittest**

- `@pytest.mark.parametrize`: 1 test → múltiples casos
- Fixtures con scopes: reutilización inteligente
- `pytest.approx()`: comparación de floats sin problemas
- `pytest.raises(match="regex")`: validación precisa de excepciones
- Clases sin herencia de `unittest.TestCase`

**5. Cobertura != líneas ejecutadas**

98% aquí significa: 6 categorías de tests, validaciones de tipo/rango, edge/corner/boundary cases, propiedades matemáticas. No es solo un número.
