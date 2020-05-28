"""Financial projection for photovailtic system."""

# Utilities
import numpy as np

# Local
from .models import FinancialCalc


# Functions
def financial_calc(energy_by_month, kwh_cost, module, inverter, system):
    """
    Returns:
        - The month money savings of electrical coute derived of pv system.
        - The investment return time of the pv system.
    """
    cost = FinancialCalc(kwh_cost, module, inverter, system)
    cost.calc_cost()
    savings = _savings(energy_by_month, kwh_cost)
    time_return = _investment_return(cost.total_cost_, savings)

    return savings, time_return


def average_paymet_to_kwh_info(average_payment, fee):
    """
    Returns:
        - The kWh cost.
        - The amount of khW consumed in the period.

    References:
    .. [1] https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRECasa/Tarifas/Tarifa1.aspx
    """

    # DAC fee
    DAC_fee = 4.34

    # Average limits in others CFE fee(s)
    limit_energy = [128, 171]

    # Cost by limit of CFE fee(s)
    fee = [0.793, 1.13, 2.964]

    # For DAC fee
    if fee == 'DAC':
        return DAC_fee, average_payment / DAC_fee

    # For other fee
    count = average_payment
    cost = []
    consume = []

    for i in range(2):
        if limit_energy[i] * fee[i] < count:
            cost.append(fee[i] * limit_energy[i])
            consume.append(limit_energy[i])
            count -= limit_energy[i]
        else:
            cost.append(fee[i] * limit_energy[i])
            consume.append(count/fee[i])

    if count > 0:
        cost.append(fee[2] * count)
        consume.append(count/fee[2])

    # Toal
    mean_consume = np.sum(np.array(consume))
    # weighted average
    kWh_cost = np.mean(np.array(cost)) / mean_consume

    return kWh_cost, mean_consume


def _savings(energy_by_month, kwh_cost):
    """
    Returns savings by month.
    """

    savings = {}
    for month, energy in energy_by_month.items():
        savings[month] = energy*kwh_cost

    return savings


def _investment_return(total_cost, savings):
    """
    Returns investment return time.
    """

    # Simple return
    anual_savigs = np.sum(list(savings.values()))
    time = total_cost/anual_savigs

    return time
