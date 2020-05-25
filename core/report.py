"""
Make all the calculations and return data for show in template.
"""

# Utilities
import pandas as pd
import numpy as np

# Local
from core.energy.output_energy import output_power
from core.financial.projection import financial_calc


# Energy Report
def energy_report(latitude, longitude, width, height):
    """
    Returns:
        - The energy output by month derived from pv system.
        - The total energy arrived from sum to pv system.
        - The array (type and number of modules, type and number of inverters)
    """

    power_ouput, effective_radiation, array = output_power(
        latitude=latitude,
        longitude=longitude,
        width=width,
        height=height
    )

    # Convert power to energy
    irrad_energy_by_month = _power_to_energy(effective_radiation)
    energy_ouput_by_month = _power_to_energy(power_ouput)

    return {
        'output': energy_ouput_by_month,
        'irrad': irrad_energy_by_month,
        'array': array
    }


def financial_report(energy_report, kwh_cost):
    """
    Returns a tuple with savings by month and the
    investment return time.
    """

    financial_info = financial_calc(
        energy_report['output'],
        kwh_cost=kwh_cost,
        module=energy_report['array']['module'][1],
        inverter=energy_report['array']['inverter'][1],
        system=(
            energy_report['array']['module'][0],
            energy_report['array']['inverter'][0]
        )
    )

    return financial_info


def _power_to_energy(power):
    """
    Returns a dict withthe total energy bymonth
    derivend from the power of sun or pv system.
    """
    months = _generate_months()
    data_by_month = {}

    for name, num in months.items():
        sum_month = _get_month(power, num).values
        sum_month = np.trapz(sum_month)
        data_by_month[name] = sum_month/1000

    return data_by_month


def _generate_months():
    """
    Return a Dict with name and number of months.
    """

    months_name = [
        'Ene', 'Feb', 'Mar', 'Abr',
        'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dic'
    ]

    month_num = np.arange(1, 13)

    return dict(zip(months_name, month_num))


def _get_month(data, month):
    """
    Returns the values by month of DataFrame.
    """

    mask = (data.index.month == month)

    return data[mask]
