"""Info for photovoltaic system cost."""

# Local
from core.energy.output_energy import PTC_POWER_MODULE


# Typical prices for fotovoltaic components:
# Prices finded on SunWatts: https://sunwatts.com/
MODULES = {
    # model_name : prices in MXN.

    'SunPower_SPR_305_WHT___2009_': 5400,
}

INVERTERS = {
    # model_name : prices in MXN.

    'ABB__PVI_CENTRAL_50_US__480V_': 92500,
    'ABB__TRIO_20_0_TL_OUTD_S1B_US_480__480V_': 39089,
    'ABB__UNO_8_6_TL_OUTD_S_US_A__240V_': 19055,
    'ABB__PVI_3_0_OUTD_S_US_A__240V_': 8815,
    'ABB__MICRO_0_3_I_OUTD_US_240__240V_': 4007,
}

# Aditional costs, info by NREL: U.S. Solar Photovoltaic System Cost Benchmark: Q1 2018
STRUCTURE_PRICE = 2  # MXN per Watt installed
ELCTRICAL_BOS_PRICE = 4  # MXN per Watt installed
INSTALATION = 0.2  # Percentage of the total cost

# Conversions
kW_to_W = 1000


# Functions
def find_price_module(module_model):
    """
    Returns the price of the module.
    """

    if module_model in MODULES:
        return MODULES[module_model]
    else:
        raise 'The module does not in database'


def find_price_inverter(inverter_model):
    """
    Returns the price of the inverter.
    """

    if inverter_model in INVERTERS:
        return INVERTERS[inverter_model]
    else:
        raise 'The inverter does not in database'


def structure_cost(num_modules):
    """
    Returns the cost of photovoltaic structure.
    """

    total_installed_power = num_modules * PTC_POWER_MODULE * kW_to_W

    return STRUCTURE_PRICE * total_installed_power


def electrical_bos_cost(num_modules):
    """
    Returns the cost of aditional electrical components.
    """

    total_installed_power = num_modules * PTC_POWER_MODULE * kW_to_W

    return ELCTRICAL_BOS_PRICE * total_installed_power


def instalation_cost(system_cost):
    """
    Returns the instalation costs.
    """
    return system_cost * INSTALATION
