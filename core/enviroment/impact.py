"""
Calculates the positive environmental impact derived 
from the installation of the proposed photovoltaic system.
"""


# Functions
def co2_evited(anual_energy_by_pv_system):
    """
    Returns the anual CO2 eliminated by the emissions
    reduction derived from photovoltaic system in kilograms of CO2.

    Reference:
    [1] ""
    """

    co2_eliminated_per_year = anual_energy_by_pv_system*0.9
    return co2_eliminated_per_year
