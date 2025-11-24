def calculate_compound_interest(principal, rate, periods):
    """
    Calcula el valor futuro usando interés compuesto.
    
    Fórmula: FV = PV × (1 + r)^n
    
    Args:
        principal (float): Monto inicial. Puede ser:
            - Positivo: inversión o activo
            - Negativo: deuda o pasivo
            - Cero: sin capital inicial
        rate (float): Tasa de interés por período en decimal. Puede ser:
            - Positivo: crecimiento (ej: 5% = 0.05)
            - Negativo: depreciación o decrecimiento (ej: -5% = -0.05)
            - Cero: sin cambio
            - DEBE SER > -1 (pérdida del 100% o mayor es indefinida)
        periods (float): Número de períodos. Debe ser >= 0. Puede ser:
            - Entero: períodos completos
            - Fraccionario: períodos parciales (ej: 2.5 años)
    
    Returns:
        float: Valor futuro después de aplicar interés compuesto
    
    Raises:
        TypeError: Si algún argumento no es numérico (int o float)
        ValueError: Si rate <= -1 o periods < 0
    
    Examples:
        >>> calculate_compound_interest(1000, 0.05, 5)
        1276.2815625
        
        >>> calculate_compound_interest(1000, 0, 5)
        1000.0
        
        >>> calculate_compound_interest(-10000, 0.05, 5)
        -12762.815625  # Deuda crece con intereses
        
        >>> calculate_compound_interest(20000, -0.15, 5)
        8874.10875  # Depreciación del activo
    
    Notes:
        - Para principal negativo: representa deudas que crecen con intereses
        - Para rate negativo: representa depreciación o decrecimiento
        - Para periods = 0: retorna el principal sin cambios
        - Rate = -1 es el límite matemático (división por cero)
    """
    # Validar tipos
    if not isinstance(principal, (int, float)):
        raise TypeError(
            f"principal debe ser numérico (int o float), "
            f"recibido: {type(principal).__name__}"
        )
    
    if not isinstance(rate, (int, float)):
        raise TypeError(
            f"rate debe ser numérico (int o float), "
            f"recibido: {type(rate).__name__}"
        )
    
    if not isinstance(periods, (int, float)):
        raise TypeError(
            f"periods debe ser numérico (int o float), "
            f"recibido: {type(periods).__name__}"
        )
    
    # Validar rate (límite matemático)
    if rate <= -1:
        raise ValueError(
            f"rate debe ser > -1 (recibido: {rate}). "
            f"Una tasa de -100% o menor es matemáticamente indefinida: "
            f"(1 + rate)^n = (1 + {rate})^n = {1 + rate}^n"
        )
    
    # Validar periods (lógica financiera)
    if periods < 0:
        raise ValueError(
            f"periods debe ser >= 0 (recibido: {periods}). "
            f"Para calcular valores pasados, use una función de valor presente."
        )
    
    # Cálculo del interés compuesto
    return principal * ((1 + rate) ** periods)

def calculate_annuity_payment(principal, rate, periods):
    """
    Calcula el pago periódico de una anualidad (préstamo/inversión) con tasa de interés compuesta.
    
    Fórmula: PMT = P × [r × (1 + r)^n] / [(1 + r)^n - 1]
    Caso especial: Si r = 0, entonces PMT = P / n
    
    Args:
        principal (float): Monto del préstamo o inversión. Debe ser >= 0.
            - Representa el valor presente de la anualidad
            - No puede ser negativo (no existe préstamo negativo)
        rate (float): Tasa de interés por período en decimal. Debe ser >= 0.
            - Positivo: interés normal (ej: 5% = 0.05)
            - Cero: sin interés (pago simple = principal / períodos)
            - No puede ser negativo (no aplica en anualidades)
        periods (float): Número de períodos de pago. Debe ser > 0.
            - Entero: períodos completos
            - Fraccionario: períodos parciales (menos común)
            - Al menos 1 período requerido
    
    Returns:
        float: Pago periódico requerido para amortizar el principal
    
    Raises:
        TypeError: Si algún argumento no es numérico (int o float)
        ValueError: Si principal < 0, rate < 0, o periods <= 0
    
    Examples:
        >>> calculate_annuity_payment(10000, 0.05, 12)
        1128.25  # Pago mensual para préstamo de $10k al 5%
        
        >>> calculate_annuity_payment(12000, 0.0, 12)
        1000.0  # Sin interés, pago simple
        
        >>> calculate_annuity_payment(0, 0.05, 12)
        0.0  # Sin principal, sin pago
    
    Notes:
        - Usado para calcular pagos de préstamos, hipotecas, anualidades
        - El pago cubre tanto principal como intereses
        - Total pagado = PMT × n (será > principal si rate > 0)
        - Para rate = 0, se usa división simple para evitar indefinición matemática
    """
    # Validar tipos
    if not isinstance(principal, (int, float)):
        raise TypeError(
            f"principal debe ser numérico (int o float), "
            f"recibido: {type(principal).__name__}"
        )
    
    if not isinstance(rate, (int, float)):
        raise TypeError(
            f"rate debe ser numérico (int o float), "
            f"recibido: {type(rate).__name__}"
        )
    
    if not isinstance(periods, (int, float)):
        raise TypeError(
            f"periods debe ser numérico (int o float), "
            f"recibido: {type(periods).__name__}"
        )
    
    # Validar principal (no puede ser negativo en anualidades)
    if principal < 0:
        raise ValueError(
            f"principal debe ser >= 0 (recibido: {principal}). "
            f"Una anualidad no puede tener monto negativo."
        )
    
    # Validar rate (no puede ser negativo en anualidades)
    if rate < 0:
        raise ValueError(
            f"rate debe ser >= 0 (recibido: {rate}). "
            f"Las anualidades no admiten tasas de interés negativas."
        )
    
    # Validar periods (debe ser al menos 1)
    if periods <= 0:
        raise ValueError(
            f"periods debe ser > 0 (recibido: {periods}). "
            f"Se requiere al menos un período de pago."
        )
    
    # Caso especial: tasa cero (evita división por cero en fórmula)
    if rate == 0:
        return principal / periods
    
    # Cálculo estándar de anualidad
    return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)

def calculate_internal_rate_of_return(cash_flows, iterations=100):
    """
    Calcula la Tasa Interna de Retorno (TIR/IRR) usando el método de Newton-Raphson.
    
    La TIR es la tasa de descuento que hace que el NPV sea cero:
    NPV = Σ[CFt / (1 + IRR)^t] = 0
    
    Args:
        cash_flows (list): Lista de flujos de efectivo. Debe contener:
            - Al menos 2 elementos (inversión y retorno)
            - Al menos un flujo negativo (inversión/costo)
            - Al menos un flujo positivo (retorno/ingreso)
            - Típicamente: primer elemento negativo (inversión inicial)
        iterations (int): Número máximo de iteraciones para convergencia.
            - Debe ser > 0
            - Default: 100 (suficiente para la mayoría de casos)
    
    Returns:
        float: Tasa Interna de Retorno (TIR) como decimal
            - Positivo: inversión rentable
            - Cero: break-even (recupera exactamente el capital)
            - Negativo: inversión con pérdida
    
    Raises:
        TypeError: Si cash_flows no es una lista/iterable o contiene no-numéricos
        ValueError: Si cash_flows < 2 elementos, todos positivos, todos negativos,
                   o iterations <= 0
    
    Examples:
        >>> calculate_internal_rate_of_return([-1000, 1200], iterations=100)
        0.20  # 20% de retorno
        
        >>> calculate_internal_rate_of_return([-1000, 1000])
        0.0  # Break-even
        
        >>> calculate_internal_rate_of_return([-1000, 300, 300, 300, 300, 300])
        0.15  # 15% de retorno aproximadamente
    
    Notes:
        - Usa el método iterativo de Newton-Raphson
        - Puede no converger si cash flows son erráticos
        - Flujos con múltiples cambios de signo pueden tener múltiples TIRs
        - Comienza con guess inicial de 10% (0.1)
    """
    # Validar tipo de cash_flows
    if not isinstance(cash_flows, (list, tuple)):
        raise TypeError(
            f"cash_flows debe ser una lista o iterable, "
            f"recibido: {type(cash_flows).__name__}"
        )
    
    # Convertir a lista si es necesario
    cash_flows_list = list(cash_flows)
    
    # Validar cantidad mínima de flujos
    if len(cash_flows_list) < 2:
        raise ValueError(
            f"cash_flows debe tener al menos 2 elementos "
            f"(inversión y retorno), recibido: {len(cash_flows_list)}"
        )
    
    # Validar que todos sean numéricos
    for i, cf in enumerate(cash_flows_list):
        if not isinstance(cf, (int, float)):
            raise TypeError(
                f"Todos los elementos de cash_flows deben ser numéricos. "
                f"Elemento en índice {i} es {type(cf).__name__}"
            )
    
    # Validar que haya al menos un flujo negativo y uno positivo
    has_negative = any(cf < 0 for cf in cash_flows_list)
    has_positive = any(cf > 0 for cf in cash_flows_list)
    
    if not has_negative:
        raise ValueError(
            "cash_flows debe haber al menos un flujo negativo (inversión/costo)"
        )
    
    if not has_positive:
        raise ValueError(
            "cash_flows debe haber al menos un flujo positivo (retorno/ingreso)"
        )
    
    # Validar iterations
    if not isinstance(iterations, int):
        raise TypeError(
            f"iterations debe ser un entero, recibido: {type(iterations).__name__}"
        )
    
    if iterations <= 0:
        raise ValueError(
            f"iterations debe ser > 0, recibido: {iterations}"
        )
    
    # Método de Newton-Raphson
    guess = 0.1  # Guess inicial: 10%
    
    for _ in range(iterations):
        # Calcular NPV con el guess actual
        npv = sum(cf / (1 + guess) ** i for i, cf in enumerate(cash_flows_list))
        
        # Calcular la derivada del NPV
        derivative = sum(-i * cf / (1 + guess) ** (i + 1) for i, cf in enumerate(cash_flows_list))
        
        # Si la derivada es cero, no podemos continuar
        if derivative == 0:
            break
        
        # Actualizar el guess usando Newton-Raphson
        guess -= npv / derivative
    
    return guess
