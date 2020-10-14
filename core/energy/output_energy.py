"""Output DC energy and power calculatons."""

# PvLib
from pvlib.pvsystem import sapm_effective_irradiance

# Utilitites
import numpy as np
import pandas as pd

# Local
from .models import Module, Inverter
from .solar_energy import solar_radiation, _air_mass


# Solar module by dafault
MODULE = 'SunPower_SPR_305_WHT___2009_'
PTC_POWER_MODULE = 0.3  # kWp

# Inverter options
INVERTERS_INF0 = {
    'ABB__MICRO_0_3_I_OUTD_US_240__240V_': {
        'name': 'ABB__MICRO_0_3_I_OUTD_US_240__240V_',
        'normal_name': 'ABB-MICRO_240V',
        'power': 300,
    },
    'ABB__PVI_3_0_OUTD_S_US_A__240V_': {
        'name': 'ABB__PVI_3_0_OUTD_S_US_A__240V_',
        'normal_name': 'ABB-ABB_PVI_240V',
        'power': 3000,
    },
    'ABB__UNO_8_6_TL_OUTD_S_US_A__240V_': {
        'name': 'ABB__UNO_8_6_TL_OUTD_S_US_A__240V_',
        'normal_name': 'ABB-ABB_UNO_240V',
        'power': 9000,
    },
    'ABB__UNO_8_6_TL_OUTD_S_US_A__240V_': {
        'name': 'ABB__UNO_8_6_TL_OUTD_S_US_A__240V_',
        'normal_name': 'ABB-ABB_UNO_240V',
        'power': 27000,
    },
    'ABB__PVI_CENTRAL_50_US__480V_': {
        'name': 'ABB__PVI_CENTRAL_50_US__480V_',
        'normal_name': 'ABB_PVI_CENTRAL_480V',
        'power': 50000,
    },
}


# Calculations for AC power output
def output_power(latitude, longitude, width, height):
    """
    Make calculations for total AC power output and returns:
        - AC power output by hour in a year.
        - The effective radiation used by the photovoltaic system.
        - The data of the pv system:
            (number of panels, type and number of inverters.)
    """

    # Get solar info
    solar_info = solar_radiation(latitude, longitude)

    # Get the module propertys
    module = Module()
    module.get_propertys(MODULE)

    # Effectiev radiation calculation
    effective_irradiance = _get_effective_irradiance(
        module_propertys=module.propertys,
        **solar_info
    )

    # Maximun or needed number of modules
    num_modules = _get_num_modules(
        width=width,
        heigth=height,
        module_area=module.propertys.Area,
        latitude=latitude
    )

    total_peak_power = _get_total_power(num_modules)
    num_modules_total = num_modules[0]*num_modules[1]

    # Inverter(s) info
    best_inverter, inverter_power = _choose_inverter(total_peak_power)
    inverter = Inverter()
    inverter.get_propertys(best_inverter)

    # Array info
    num_inverters = _get_num_inverters(
        num_modules=num_modules,
        inverter_power=inverter_power
    )

    # Power output
    power_output = effective_irradiance * PTC_POWER_MODULE * num_modules_total

    system_data = {
        'module': [num_modules_total, module.module],
        'inverter': [num_inverters, inverter.inverter],
    }

    return (power_output, effective_irradiance, system_data)


def _get_effective_irradiance(module_propertys, data, poa, am, aoi):
    """
    Returns the effective radiationused by the photovoltaic system
    at the orientation of the array.
    """

    effective_irrad = sapm_effective_irradiance(
        poa_direct=poa.poa_direct,
        poa_diffuse=poa.poa_diffuse,
        airmass_absolute=am,
        aoi=aoi,
        module=module_propertys
    )

    return effective_irrad


def _get_num_modules(width, heigth, module_area, latitude):
    """
    Calculates the number and array of modules and returns:
        - Maximun number of modules in serie.
        - Maximun number of rows.
    """

    width_module = module_area * 0.6
    heigth_module = module_area / width_module
    data = {
        'width': width,
        'heigth': heigth,
        'width_module': width_module,
        'heigth_module': heigth_module,
        'latitude': latitude
    }

    # Modules position in W-O direction (horizontal position)
    num_serie_h, num_par_h = _get_num_modules_horizontal(**data)
    total_num_h = num_serie_h * num_par_h

    # Modules position un N-S direction (vertical position)
    num_serie_v, num_par_v = _get_num_modules_vertical(**data)
    total_num_v = num_serie_v * num_par_v

    if total_num_h >= total_num_v:
        return (num_serie_h, num_par_h)
    else:
        return (num_serie_v, num_par_v)


def _get_num_modules_horizontal(width, heigth, width_module,
                                heigth_module, latitude):
    """
    Retunrs the number of modules with horizontal position.
    """

    # Modules in serie
    num_serie = _special_round(width/width_module)

    # Parallel rows:
    # Takes acount the minimun distance between row due the shadows.
    height_system = heigth_module * np.sin(np.radians(latitude))
    large_system = heigth_module * np.cos(np.radians(latitude))
    separation_row = height_system/np.tan(np.radians(61-latitude))
    total_separation_row = separation_row + large_system

    num_par = _special_round(heigth/total_separation_row)

    return num_serie, num_par


def _get_num_modules_vertical(width, heigth, width_module,
                              heigth_module, latitude):
    """
    Retunrs the number of modules with vertical position.
    """

    # Modules in serie
    num_serie = _special_round(width/heigth_module)

    # Parallel rows:
    # Takes acount the minimun distance between row due the shadows.
    height_system = width_module * np.sin(np.radians(latitude))
    large_system = width_module * np.cos(np.radians(latitude))
    separation_row = height_system/np.tan(np.radians(61-latitude))
    total_separation_row = separation_row + large_system

    num_par = _special_round(heigth/total_separation_row)

    return num_serie, num_par


def _special_round(num):
    """
    Returns the round number:
        - if decimal is equal or higher than .85 it is rounded up
        - else it is rounded down.
    """

    from math import floor

    num_int = floor(num)
    decimal = num - num_int

    if num_int < 1:
        return 1
    else:
        if decimal >= 0.85:
            return num_int + 1
        else:
            return num_int


def _get_num_inverters(num_modules, inverter_power):
    """
    Returns number of inverters.
    """

    from math import ceil

    TotalPower = _get_total_power(num_modules)
    num_inverters = ceil(TotalPower/inverter_power)

    return num_inverters


def _get_total_power(num_modules):
    """
    Returns the total peak power by all pv system.
    """

    kW_to_W = 1000
    total_modules = num_modules[0] * num_modules[1]
    TotalPower = PTC_POWER_MODULE * total_modules * kW_to_W

    return TotalPower


def _choose_inverter(TotalPower):
    """
    Returns the inverter that best matches
    the calculated pv system.
    """

    if TotalPower >= 40000:
        _inverter = INVERTERS_INF0['ABB__PVI_CENTRAL_50_US__480V_']['name']
        inverter_power = INVERTERS_INF0['ABB__PVI_CENTRAL_50_US__480V_']['power']

    elif TotalPower >= 20000:
        _inverter = INVERTERS_INF0['ABB__UNO_8_6_TL_OUTD_S_US_A__240V_']['name']
        inverter_power = INVERTERS_INF0['ABB__UNO_8_6_TL_OUTD_S_US_A__240V_']['power']

    elif TotalPower >= 10000:
        _inverter = INVERTERS_INF0['ABB__UNO_8_6_TL_OUTD_S_US_A__240V_']['name']
        inverter_power = INVERTERS_INF0['ABB__UNO_8_6_TL_OUTD_S_US_A__240V_']['power']

    elif TotalPower >= 4000:
        _inverter = INVERTERS_INF0['ABB__PVI_3_0_OUTD_S_US_A__240V_']['name']
        inverter_power = INVERTERS_INF0['ABB__PVI_3_0_OUTD_S_US_A__240V_']['power']

    else:
        _inverter = INVERTERS_INF0['ABB__MICRO_0_3_I_OUTD_US_240__240V_']['name']
        inverter_power = INVERTERS_INF0['ABB__MICRO_0_3_I_OUTD_US_240__240V_']['power']

    return _inverter, inverter_power
