"""Solaru app models."""

# Utilities
import numpy as np

# Local
from core.enviroment.impact import co2_evited
from core.report import financial_report, energy_report
from core.financial.projection import average_paymet_to_kwh_info
from core.energy.models import ERROR_PVGIS_REQUEST


# Models
class CalcActive:
    """
    Class to manage the interaction beetwen the
    UI and backend for solar calculations.
    """

    def __init__(self):
        self.is_active = False

    def activate(self, latitude, longitude, width, height, average_payment):
        """
        Make all the calculations and save it in the object to show in template.
        """
        self.is_active = True

        kwh_cost, mean_consume = average_paymet_to_kwh_info(average_payment)

        self.get_info(
            latitude=latitude,
            longitude=longitude,
            width=width,
            height=height,
            kwh_cost=kwh_cost,
            mean_consume=mean_consume
        )

    def get_info(self, latitude, longitude, width, height, kwh_cost, mean_consume):
        self.energy = energy_report(latitude, longitude, width, height)
        self.finance = financial_report(self.energy, kwh_cost)
        self.output = dict_to_list(self.energy['output'])
        self.irrad = dict_to_list(self.energy['irrad'])
        self.savings = dict_to_list(self.finance[0])
        self.period_return = round_data(self.finance[1])

        self.num_modules = self.energy['array']['module'][0]
        self.name_modules = self.energy['array']['module'][1]
        self.num_inverters = self.energy['array']['inverter'][0]
        self.name_inverter = self.energy['array']['inverter'][1]

        self.consume = mean_consume*6
        self.total_cost = self.consume*kwh_cost
        self.total_saving = get_total_year(self.savings)
        self.total_output = get_total_year(self.output)
        self.cost_system = round(self.total_saving * self.period_return)
        self.co2 = round_data(co2_evited(self.total_output))

        self.error_request = ERROR_PVGIS_REQUEST

        self.energy_from_sun, self.energy_from_network = _make_percentage_energy(
            self.consume,
            self.total_output
        )


def dict_to_list(dict):
    """
    Returns list from dict values.
    """

    li = list(dict.values())
    li = np.array(li)

    return list(round_data(li))


def get_total_year(data_by_month):
    """
    Returns the magnitud of a values per month for all year.
    """

    total_per_year = np.sum(np.asarray(data_by_month))

    return round_data(total_per_year)


def round_data(data):
    """
    Returns rounded data with 2 decimals.
    """

    return np.around(data, decimals=2)


def _make_percentage_energy(network, sun):
    """
    Calculates the percentage of the energy
    consumed by the electrical network and
    by solar system.
    """

    sun_percentage = sun/network
    network_percentage = 1 - sun_percentage

    if sun_percentage >= 1:
        return 1, 0
    else:
        return sun_percentage, network_percentage
