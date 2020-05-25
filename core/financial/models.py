"""Models for financial calculations."""

# Local
from .system_cost import (
    find_price_inverter,
    find_price_module,
    instalation_cost,
    electrical_bos_cost,
    structure_cost
)


# Models
class FinancialCalc:
    """
    Class for make all cost calculations.
    """

    def __init__(self, kwh_cost, module, inverter, system):
        self.kwh_cost = kwh_cost
        self.module = module
        self.number_modules = system[0]
        self.inverter = inverter
        self.number_inverters = system[1]

    def calc_cost(self):
        self.system_cost()
        self.total_cost()

    def system_cost(self):
        self.find_cost()
        self.structure_cost = structure_cost(
            num_modules=self.number_modules
        )

        self.electrical_cost = electrical_bos_cost(
            num_modules=self.number_modules
        )

        self.system_cost_ = (
            self.electrical_cost +
            self.structure_cost +
            self.module_cost * self.number_modules +
            self.inverter_cost * self.number_inverters
        )

    def find_cost(self):
        self.module_cost = find_price_module(self.module)
        self.inverter_cost = find_price_inverter(self.inverter)

    def total_cost(self):
        self.instalation_cost_ = instalation_cost(self.system_cost_)
        self.total_cost_ = self.system_cost_ + self.instalation_cost_
