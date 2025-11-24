"""
Suite completa de tests para el módulo finance.py
Implementa TDD (Test-Driven Development) con pytest.

Este archivo contiene 91 tests que cubren las 3 funciones del módulo finance:
- calculate_compound_interest: 29 tests
- calculate_annuity_payment: 31 tests
- calculate_internal_rate_of_return: 31 tests

"""
import pytest
from finance import (
    calculate_compound_interest,
    calculate_annuity_payment,
    calculate_internal_rate_of_return
)


# ============================================================================
# SECCIÓN 1: TESTS PARA calculate_compound_interest
# ============================================================================

# ----------------------------------------------------------------------------
# FIXTURES para calculate_compound_interest
# ----------------------------------------------------------------------------

@pytest.fixture
def standard_investment():
    """Fixture: inversión estándar de 10 años al 7%."""
    return {"principal": 10000, "rate": 0.07, "periods": 10}


@pytest.fixture
def small_investment():
    """Fixture: inversión pequeña para verificar precisión."""
    return {"principal": 100, "rate": 0.05, "periods": 5}


@pytest.fixture(params=[0.05, 0.10, 0.15, 0.20])
def various_rates(request):
    """Fixture parametrizada con múltiples tasas."""
    return request.param


@pytest.fixture
def debt_scenario():
    """Fixture: escenario de deuda (principal negativo)."""
    return {"principal": -10000, "rate": 0.05, "periods": 5}


@pytest.fixture
def depreciation_scenario():
    """Fixture: escenario de depreciación (tasa negativa)."""
    return {"principal": 10000, "rate": -0.03, "periods": 10}


# ----------------------------------------------------------------------------
# TESTS: calculate_compound_interest
# ----------------------------------------------------------------------------

class TestCompoundInterestHappyPath:
    """Tests con valores normales y esperados."""
    
    def test_basic_compound_interest_one_period(self):
        """Test básico: $1000 al 5% por 1 período."""
        result = calculate_compound_interest(1000, 0.05, 1)
        assert result == pytest.approx(1050.0)
    
    def test_basic_compound_interest_multiple_periods(self):
        """Test: $1000 al 5% por 5 períodos."""
        result = calculate_compound_interest(1000, 0.05, 5)
        assert result == pytest.approx(1276.2815625, rel=1e-9)
    
    def test_standard_investment_scenario(self, standard_investment):
        """Test usando fixture: inversión estándar a largo plazo."""
        result = calculate_compound_interest(**standard_investment)
        expected = 10000 * (1.07 ** 10)
        assert result == pytest.approx(expected, rel=1e-9)
        assert result > standard_investment["principal"]
        assert result == pytest.approx(19671.51, rel=1e-4)
    
    @pytest.mark.parametrize("rate", [0.05, 0.10, 0.15, 0.20])
    def test_different_rates_same_principal(self, rate):
        """Test parametrizado: mismo principal, diferentes tasas."""
        result = calculate_compound_interest(1000, rate, 5)
        assert result > 1000
        expected = 1000 * (1 + rate) ** 5
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_large_principal_small_rate(self):
        """Test: capital grande con tasa pequeña."""
        result = calculate_compound_interest(1000000, 0.02, 10)
        expected = 1000000 * (1.02 ** 10)
        assert result == pytest.approx(expected, rel=1e-9)


class TestCompoundInterestEdgeCases:
    """Tests con valores límite."""
    
    def test_zero_principal(self):
        """Test: principal cero resulta en cero."""
        result = calculate_compound_interest(0, 0.05, 5)
        assert result == 0.0
    
    def test_zero_rate(self):
        """Test: tasa cero mantiene el principal."""
        result = calculate_compound_interest(1000, 0, 5)
        assert result == 1000.0
    
    def test_zero_periods(self):
        """Test: cero períodos mantiene el principal."""
        result = calculate_compound_interest(1000, 0.05, 0)
        assert result == 1000.0
    
    def test_single_period(self):
        """Test: un solo período es interés simple."""
        result = calculate_compound_interest(1000, 0.05, 1)
        assert result == pytest.approx(1050.0)


class TestCompoundInterestCornerCases:
    """Tests con combinaciones extremas."""
    
    def test_all_zeros(self):
        """Test: todos los parámetros en cero."""
        result = calculate_compound_interest(0, 0, 0)
        assert result == 0.0
    
    def test_very_small_values(self):
        """Test: valores muy pequeños."""
        result = calculate_compound_interest(0.01, 0.01, 1)
        assert result == pytest.approx(0.0101, rel=1e-9)
    
    def test_rate_of_one_hundred_percent(self):
        """Test: tasa del 100% (duplica cada período)."""
        result = calculate_compound_interest(1000, 1.0, 3)
        assert result == pytest.approx(8000.0, rel=1e-9)


class TestCompoundInterestNegativeCases:
    """Tests con valores negativos y casos de error."""
    
    def test_invalid_type_principal(self):
        """Test que verifica rechazo de tipos inválidos para principal."""
        with pytest.raises(TypeError, match="principal debe ser numérico"):
            calculate_compound_interest("1000", 0.05, 5)
    
    def test_invalid_type_rate(self):
        """Test que verifica rechazo de tipos inválidos para rate."""
        with pytest.raises(TypeError, match="rate debe ser numérico"):
            calculate_compound_interest(1000, "0.05", 5)
    
    def test_invalid_type_periods(self):
        """Test que verifica rechazo de tipos inválidos para periods."""
        with pytest.raises(TypeError, match="periods debe ser numérico"):
            calculate_compound_interest(1000, 0.05, "5")
    
    def test_negative_principal_represents_debt(self):
        """Test: principal negativo representa una DEUDA."""
        deuda = -10000
        rate = 0.05
        periods = 5
        result = calculate_compound_interest(deuda, rate, periods)
        expected = deuda * (1 + rate) ** periods
        assert result < 0
        assert abs(result) > abs(deuda)
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_negative_rate_represents_depreciation(self):
        """Test: tasa negativa representa DEPRECIACIÓN."""
        principal = 10000
        rate = -0.03
        periods = 10
        result = calculate_compound_interest(principal, rate, periods)
        expected = principal * (1 + rate) ** periods
        assert result < principal
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_rate_equals_minus_one_raises_error(self):
        """Test: rate = -1 causa división por cero."""
        with pytest.raises(ValueError, match="rate debe ser > -1"):
            calculate_compound_interest(1000, -1.0, 5)
    
    def test_rate_less_than_minus_one_raises_error(self):
        """Test: rate < -1 es inválido."""
        with pytest.raises(ValueError, match="rate debe ser > -1"):
            calculate_compound_interest(1000, -1.5, 5)
    
    def test_negative_periods_raises_error(self):
        """Test: períodos negativos no tienen sentido."""
        with pytest.raises(ValueError, match="periods debe ser >= 0"):
            calculate_compound_interest(1000, 0.05, -5)


class TestCompoundInterestBoundaries:
    """Tests en fronteras de rangos válidos."""
    
    def test_fractional_periods(self):
        """Test: períodos fraccionarios (interés compuesto continuo)."""
        result = calculate_compound_interest(1000, 0.05, 2.5)
        expected = 1000 * (1.05 ** 2.5)
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_very_large_periods(self):
        """Test: cantidad grande de períodos."""
        result = calculate_compound_interest(1000, 0.01, 100)
        expected = 1000 * (1.01 ** 100)
        assert result == pytest.approx(expected, rel=1e-9)
    
    def test_rate_approaching_minus_one(self):
        """Test: tasa muy cercana a -1 pero válida."""
        result = calculate_compound_interest(1000, -0.99, 2)
        expected = 1000 * (0.01 ** 2)
        assert result == pytest.approx(expected, rel=1e-9)


class TestCompoundInterestMathematicalProperties:
    """Tests de propiedades matemáticas."""
    
    def test_idempotency(self):
        """Test: aplicar 1 período dos veces = 2 períodos."""
        result_once = calculate_compound_interest(1000, 0.05, 1)
        result_twice = calculate_compound_interest(result_once, 0.05, 1)
        result_direct = calculate_compound_interest(1000, 0.05, 2)
        assert result_twice == pytest.approx(result_direct, rel=1e-9)
    
    def test_monotonicity_with_rate(self):
        """Test: mayor tasa → mayor valor futuro."""
        result_low = calculate_compound_interest(1000, 0.05, 5)
        result_high = calculate_compound_interest(1000, 0.10, 5)
        assert result_high > result_low
    
    def test_monotonicity_with_periods(self):
        """Test: más períodos → mayor valor futuro (con tasa positiva)."""
        result_short = calculate_compound_interest(1000, 0.05, 5)
        result_long = calculate_compound_interest(1000, 0.05, 10)
        assert result_long > result_short


# ============================================================================
# SECCIÓN 2: TESTS PARA calculate_annuity_payment
# ============================================================================

# ----------------------------------------------------------------------------
# FIXTURES para calculate_annuity_payment
# ----------------------------------------------------------------------------

@pytest.fixture
def standard_loan():
    """Fixture: préstamo estándar de 12 meses al 5%."""
    return {"principal": 10000, "rate": 0.05, "periods": 12}


@pytest.fixture
def mortgage_30_years():
    """Fixture: hipoteca de 30 años (360 pagos mensuales)."""
    return {"principal": 200000, "rate": 0.004167, "periods": 360}


@pytest.fixture(params=[0.03, 0.05, 0.07, 0.10])
def various_loan_rates(request):
    """Fixture parametrizada con múltiples tasas."""
    return request.param


# ----------------------------------------------------------------------------
# TESTS: calculate_annuity_payment
# ----------------------------------------------------------------------------

class TestAnnuityPaymentHappyPath:
    """Tests con valores normales y esperados."""
    
    def test_basic_annuity_payment(self):
        """Test básico: préstamo de $10,000 al 5% mensual por 12 meses."""
        result = calculate_annuity_payment(10000, 0.05, 12)
        assert result > 0
        assert result > 10000 / 12
    
    def test_standard_loan(self, standard_loan):
        """Test usando fixture: préstamo estándar."""
        result = calculate_annuity_payment(**standard_loan)
        assert result > 0
        total_paid = result * standard_loan["periods"]
        assert total_paid > standard_loan["principal"]
    
    def test_mortgage_scenario(self, mortgage_30_years):
        """Test: hipoteca a 30 años."""
        result = calculate_annuity_payment(**mortgage_30_years)
        assert result > 0
        assert result == pytest.approx(1073.64, rel=1e-3)
    
    @pytest.mark.parametrize(
        "scenario",
        [
            {"principal": 5000, "rate": 0.08, "periods": 6},
            {"principal": 15000, "rate": 0.12, "periods": 24},
            {"principal": 100000, "rate": 0.05, "periods": 60}
        ],
        ids=["short_term_loan", "medium_term_high_rate", "long_term_large_principal"]
    )
    def test_various_loan_scenarios(self, scenario):
        """Test parametrizado: diversos escenarios de préstamo."""
        result = calculate_annuity_payment(**scenario)
        assert result > 0
        total_paid = result * scenario["periods"]
        assert total_paid > scenario["principal"]
    
    @pytest.mark.parametrize("rate", [0.03, 0.05, 0.07, 0.10])
    def test_payment_increases_with_rate(self, rate):
        """Test: mayor tasa → mayor pago mensual."""
        result = calculate_annuity_payment(10000, rate, 12)
        assert result > 0
        if rate > 0.03:
            lower_result = calculate_annuity_payment(10000, 0.03, 12)
            assert result > lower_result


class TestAnnuityPaymentEdgeCases:
    """Tests con valores límite."""
    
    def test_zero_rate_special_case(self):
        """Test: tasa cero usa fórmula simplificada."""
        result = calculate_annuity_payment(12000, 0, 12)
        assert result == pytest.approx(1000.0, rel=1e-9)
    
    def test_zero_principal(self):
        """Test: principal cero resulta en pago cero."""
        result = calculate_annuity_payment(0, 0.05, 12)
        assert result == 0.0
    
    def test_single_period(self):
        """Test: un solo período paga todo + interés."""
        result = calculate_annuity_payment(1000, 0.05, 1)
        assert result == pytest.approx(1050.0, rel=1e-9)
    
    def test_very_small_rate(self):
        """Test: tasa muy pequeña."""
        result = calculate_annuity_payment(10000, 0.0001, 12)
        assert result > 10000 / 12


class TestAnnuityPaymentCornerCases:
    """Tests con combinaciones extremas."""
    
    def test_zero_principal_zero_rate(self):
        """Test: principal y tasa en cero."""
        result = calculate_annuity_payment(0, 0, 12)
        assert result == 0.0
    
    def test_very_small_principal(self):
        """Test: principal muy pequeño."""
        result = calculate_annuity_payment(1, 0.05, 12)
        assert result > 0
        assert result < 1
    
    def test_very_high_rate(self):
        """Test: tasa muy alta."""
        result = calculate_annuity_payment(10000, 2.0, 12)
        assert result > 10000


class TestAnnuityPaymentNegativeCases:
    """Tests con valores negativos y casos de error."""
    
    def test_negative_principal_raises_error(self):
        """Test: principal negativo no válido para anualidades."""
        with pytest.raises(ValueError, match="principal debe ser >= 0"):
            calculate_annuity_payment(-10000, 0.05, 12)
    
    def test_negative_rate_raises_error(self):
        """Test: tasa negativa no válida para anualidades."""
        with pytest.raises(ValueError, match="rate debe ser >= 0"):
            calculate_annuity_payment(10000, -0.05, 12)
    
    def test_zero_periods_raises_error(self):
        """Test: períodos cero no válido."""
        with pytest.raises(ValueError, match="periods debe ser > 0"):
            calculate_annuity_payment(10000, 0.05, 0)
    
    def test_negative_periods_raises_error(self):
        """Test: períodos negativos no válido."""
        with pytest.raises(ValueError, match="periods debe ser > 0"):
            calculate_annuity_payment(10000, 0.05, -12)
    
    def test_invalid_type_principal_raises_error(self):
        """Test: tipo inválido para principal."""
        with pytest.raises(TypeError, match="principal debe ser numérico"):
            calculate_annuity_payment("10000", 0.05, 12)
    
    def test_invalid_type_rate_raises_error(self):
        """Test: tipo inválido para rate."""
        with pytest.raises(TypeError, match="rate debe ser numérico"):
            calculate_annuity_payment(10000, "0.05", 12)
    
    def test_invalid_type_periods_raises_error(self):
        """Test: tipo inválido para periods."""
        with pytest.raises(TypeError, match="periods debe ser numérico"):
            calculate_annuity_payment(10000, 0.05, "12")


class TestAnnuityPaymentBoundaries:
    """Tests en fronteras de rangos válidos."""
    
    def test_fractional_periods(self):
        """Test: períodos fraccionarios."""
        result = calculate_annuity_payment(10000, 0.05, 12.5)
        assert result > 0
    
    def test_very_long_term(self):
        """Test: plazo muy largo."""
        result = calculate_annuity_payment(100000, 0.005, 360)
        assert result > 0
    
    def test_very_large_principal(self):
        """Test: principal muy grande."""
        result = calculate_annuity_payment(10000000, 0.05, 120)
        assert result > 0


class TestAnnuityPaymentMathematicalProperties:
    """Tests de propiedades matemáticas."""
    
    def test_idempotency(self):
        """Test: recalcular con mismo input da mismo output."""
        result1 = calculate_annuity_payment(10000, 0.05, 12)
        result2 = calculate_annuity_payment(10000, 0.05, 12)
        assert result1 == result2
    
    def test_monotonicity_with_principal(self):
        """Test: mayor principal → mayor pago."""
        result_low = calculate_annuity_payment(5000, 0.05, 12)
        result_high = calculate_annuity_payment(10000, 0.05, 12)
        assert result_high > result_low
    
    def test_monotonicity_with_rate(self):
        """Test: mayor tasa → mayor pago."""
        result_low = calculate_annuity_payment(10000, 0.03, 12)
        result_high = calculate_annuity_payment(10000, 0.07, 12)
        assert result_high > result_low
    
    def test_total_payments_cover_principal_and_interest(self):
        """Test: pagos totales > principal (cubre interés)."""
        payment = calculate_annuity_payment(10000, 0.05, 12)
        total_paid = payment * 12
        assert total_paid > 10000


# ============================================================================
# SECCIÓN 3: TESTS PARA calculate_internal_rate_of_return
# ============================================================================

# ----------------------------------------------------------------------------
# FIXTURES para calculate_internal_rate_of_return
# ----------------------------------------------------------------------------

@pytest.fixture
def simple_profitable_investment():
    """Fixture: inversión simple con retornos uniformes."""
    return [-1000, 300, 300, 300, 300, 300]


@pytest.fixture
def breakeven_investment():
    """Fixture: inversión que recupera exactamente el capital (TIR ≈ 0)."""
    return [-1000, 1000]


@pytest.fixture
def loss_making_investment():
    """Fixture: inversión con pérdida."""
    return [-1000, 200, 200, 200]


@pytest.fixture
def large_investment():
    """Fixture: inversión grande con múltiples períodos."""
    return [-50000, 10000, 12000, 15000, 18000, 20000]


# ----------------------------------------------------------------------------
# TESTS: calculate_internal_rate_of_return
# ----------------------------------------------------------------------------

class TestIRRHappyPath:
    """Tests con valores normales y esperados."""
    
    def test_simple_profitable_investment(self, simple_profitable_investment):
        """Test: inversión rentable con retornos uniformes."""
        irr = calculate_internal_rate_of_return(simple_profitable_investment)
        assert irr > 0
        assert irr == pytest.approx(0.1519, abs=0.01)
    
    def test_large_investment_scenario(self, large_investment):
        """Test: inversión grande con múltiples períodos."""
        irr = calculate_internal_rate_of_return(large_investment)
        assert irr > 0
        assert irr == pytest.approx(0.1339, abs=0.01)
    
    @pytest.mark.parametrize(
        "scenario",
        [
            {"cash_flows": [-1000, 500, 600], "expected_irr": 0.0639},
            {"cash_flows": [-5000, 2000, 2500, 1800], "expected_irr": 0.1270},
            {"cash_flows": [-1000, 300, 300, 300], "expected_irr": -0.0509}
        ],
        ids=["moderate_return", "high_return", "loss_making"]
    )
    def test_various_investment_scenarios(self, scenario):
        """Test parametrizado: diversos escenarios de inversión."""
        irr = calculate_internal_rate_of_return(scenario["cash_flows"])
        assert irr == pytest.approx(scenario["expected_irr"], abs=0.01)
    
    def test_high_return_investment(self):
        """Test: inversión con alto retorno."""
        cash_flows = [-1000, 2000, 500]
        irr = calculate_internal_rate_of_return(cash_flows)
        assert irr > 0.5
    
    def test_with_custom_iterations(self):
        """Test: usar iteraciones personalizadas."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr = calculate_internal_rate_of_return(cash_flows, iterations=50)
        assert irr > 0


class TestIRREdgeCases:
    """Tests con valores límite."""
    
    def test_breakeven_investment(self, breakeven_investment):
        """Test: inversión que recupera exactamente el capital."""
        irr = calculate_internal_rate_of_return(breakeven_investment)
        assert irr == pytest.approx(0.0, abs=0.01)
    
    def test_minimum_cash_flows(self):
        """Test: cantidad mínima de flujos (2: inversión + retorno)."""
        cash_flows = [-1000, 1200]
        irr = calculate_internal_rate_of_return(cash_flows)
        assert irr == pytest.approx(0.20, abs=0.01)
    
    def test_very_long_investment_period(self):
        """Test: inversión con muchos períodos."""
        cash_flows = [-10000] + [1500] * 20
        irr = calculate_internal_rate_of_return(cash_flows)
        assert irr > 0
    
    def test_zero_initial_investment(self):
        """Test: inversión inicial cero (caso edge extremo)."""
        with pytest.raises(ValueError, match="debe haber.*flujo negativo"):
            calculate_internal_rate_of_return([0, 500, 600, 700])


class TestIRRCornerCases:
    """Tests con combinaciones extremas."""
    
    def test_all_zero_cash_flows(self):
        """Test: todos los flujos en cero."""
        with pytest.raises(ValueError, match="debe haber.*flujo negativo"):
            calculate_internal_rate_of_return([0, 0, 0, 0])
    
    def test_very_small_cash_flows(self):
        """Test: flujos de efectivo muy pequeños."""
        cash_flows = [-1, 0.3, 0.4, 0.5]
        irr = calculate_internal_rate_of_return(cash_flows)
        assert irr > 0
    
    def test_alternating_cash_flows(self):
        """Test: flujos alternados positivos/negativos."""
        cash_flows = [-1000, 500, -200, 800, 300]
        irr = calculate_internal_rate_of_return(cash_flows)
        assert isinstance(irr, float)


class TestIRRNegativeCases:
    """Tests con valores negativos y casos de error."""
    
    def test_invalid_type_cash_flows_element(self):
        """Test que verifica rechazo de elementos no numéricos en cash_flows."""
        with pytest.raises(TypeError, match="Todos los elementos de cash_flows deben ser numéricos"):
            calculate_internal_rate_of_return([-1000, "500", 600, 700])
    
    def test_invalid_type_iterations(self):
        """Test que verifica rechazo de tipo inválido para iterations."""
        with pytest.raises(TypeError, match="iterations debe ser un entero"):
            calculate_internal_rate_of_return([-1000, 500, 600, 700], iterations="100")
    
    def test_loss_making_investment(self, loss_making_investment):
        """Test: inversión que genera pérdida."""
        irr = calculate_internal_rate_of_return(loss_making_investment)
        assert irr < 0
    
    def test_empty_cash_flows_raises_error(self):
        """Test: lista vacía no válida."""
        with pytest.raises(ValueError, match="cash_flows debe tener al menos 2 elementos"):
            calculate_internal_rate_of_return([])
    
    def test_single_cash_flow_raises_error(self):
        """Test: un solo flujo no válido."""
        with pytest.raises(ValueError, match="cash_flows debe tener al menos 2 elementos"):
            calculate_internal_rate_of_return([-1000])
    
    def test_all_positive_cash_flows_raises_error(self):
        """Test: todos positivos causa overflow."""
        with pytest.raises(ValueError, match="debe haber.*flujo negativo"):
            calculate_internal_rate_of_return([100, 200, 300, 400])
    
    def test_all_negative_cash_flows_raises_error(self):
        """Test: todos negativos causa overflow."""
        with pytest.raises(ValueError, match="debe haber.*flujo positivo"):
            calculate_internal_rate_of_return([-100, -200, -300, -400])
    
    def test_invalid_type_cash_flows_raises_error(self):
        """Test: tipo incorrecto para cash_flows."""
        with pytest.raises(TypeError, match="cash_flows debe ser una lista o iterable"):
            calculate_internal_rate_of_return("[-1000, 500, 600]")
    
    def test_negative_iterations_raises_error(self):
        """Test: iteraciones negativas no válido."""
        with pytest.raises(ValueError, match="iterations debe ser > 0"):
            calculate_internal_rate_of_return([-1000, 500, 600], iterations=-10)
    
    def test_zero_iterations_raises_error(self):
        """Test: iteraciones cero no válido."""
        with pytest.raises(ValueError, match="iterations debe ser > 0"):
            calculate_internal_rate_of_return([-1000, 500, 600], iterations=0)


class TestIRRBoundaries:
    """Tests en fronteras de rangos válidos."""
    
    def test_minimum_iterations(self):
        """Test: número mínimo de iteraciones."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr = calculate_internal_rate_of_return(cash_flows, iterations=1)
        assert isinstance(irr, float)
    
    def test_very_high_iterations(self):
        """Test: número muy alto de iteraciones."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr = calculate_internal_rate_of_return(cash_flows, iterations=1000)
        assert irr > 0
    
    def test_convergence_with_different_iterations(self):
        """Test: convergencia con diferentes iteraciones."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr_10 = calculate_internal_rate_of_return(cash_flows, iterations=10)
        irr_100 = calculate_internal_rate_of_return(cash_flows, iterations=100)
        assert irr_10 == pytest.approx(irr_100, abs=0.01)


class TestIRRMathematicalProperties:
    """Tests de propiedades matemáticas."""
    
    def test_idempotency(self):
        """Test: recalcular con mismo input da mismo output."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr1 = calculate_internal_rate_of_return(cash_flows)
        irr2 = calculate_internal_rate_of_return(cash_flows)
        assert irr1 == pytest.approx(irr2, rel=1e-9)
    
    def test_scaling_property(self):
        """Test: escalar todos los flujos no cambia TIR."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        scaled_flows = [-2000, 600, 600, 600, 600, 600]
        irr_original = calculate_internal_rate_of_return(cash_flows)
        irr_scaled = calculate_internal_rate_of_return(scaled_flows)
        assert irr_original == pytest.approx(irr_scaled, abs=0.01)
    
    def test_npv_at_irr_is_zero(self):
        """Test: NPV calculado con TIR debe ser ≈ 0."""
        cash_flows = [-1000, 300, 300, 300, 300, 300]
        irr = calculate_internal_rate_of_return(cash_flows)
        npv = sum(cf / (1 + irr) ** i for i, cf in enumerate(cash_flows))
        assert npv == pytest.approx(0.0, abs=1.0)
    
    def test_higher_returns_yield_higher_irr(self):
        """Test: mayores retornos → mayor TIR."""
        low_return = [-1000, 200, 200, 200, 200, 200]
        high_return = [-1000, 400, 400, 400, 400, 400]
        irr_low = calculate_internal_rate_of_return(low_return)
        irr_high = calculate_internal_rate_of_return(high_return)
        assert irr_high > irr_low
