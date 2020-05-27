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


def average_paymet_to_kwh_info(average_payment):
    """
    Returns:
        - The kWh cost.
        - The amount of khW consumed in the period.
    """

    kWh_cost = 2.5
    meanc_consume = average_payment / kWh_cost

    return kWh_cost, meanc_consume


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
