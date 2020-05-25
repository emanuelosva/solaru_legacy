"""Solar energy and power calculations."""

# PvLib
from pvlib.solarposition import get_solarposition
from pvlib.atmosphere import get_relative_airmass, get_absolute_airmass
from pvlib.irradiance import (
    get_extra_radiation,
    haydavies, get_ground_diffuse,
    aoi,
    poa_components
)

# Utilitties
import numpy as np
import pandas as pd

# Local
from .models import PvgisRequest


# Logic for calculation solar radiation
def solar_radiation(latitude, longitude):
    """
    All calculations for solar radiation and returns:
        - Meteorological data by hour of the TMY.
        - Solar radiation by hour adjusted at plane of array.
        - Absolute airmass by ahour.
        - The angle of incidence at best array orientation. 
    """

    # Get meteorological an solar info
    pvgis_request = PvgisRequest(latitude, longitude)
    data = pvgis_request.get()

    # Extra solar info calculations (geometry and airmass)
    solar_position = _solar_position(data)
    air_mass = _air_mass(solar_position.apparent_zenith, data.data.SP)

    # Adjust solar radiation to pv system orientation
    poa, aoi = _get_poa(data, solar_position)

    solar_radiation_info = {
        'data': data,
        'poa': poa,
        'am': air_mass,
        'aoi': aoi
    }

    return solar_radiation_info


def _solar_position(data):
    """
    Returns solar geometry calculations.
    """

    # Algoritm from Pvlib
    solar_position = get_solarposition(
        time=data.data.index,
        latitude=data.latitude,
        longitude=data.longitude,
        altitude=data.elevation,
        pressure=data.data.SP,
        method='nrel_numpy',
        temperature=data.data.T2m
    )

    return solar_position


def _air_mass(zenith, pressure):
    """
    Returns the absolute air mass.
    """

    # Methods from PvLib
    rel_am = get_relative_airmass(zenith=zenith)
    abs_am = get_absolute_airmass(rel_am, pressure=pressure)

    return abs_am


def _get_poa(data, solar_position):
    """
    Return the radiation adjusted to 
    Plane of Array (SkyDiffuse, GroundDiffuse, Total).
    """

    extra_radiation = get_extra_radiation(data.data.index)

    # Best orientation for pv system
    surface_tilt = _surface_tilt(data.latitude)
    surface_azimuth = _surface_azimuth(data.latitude)

    # Sky Diffuse radiation (From PvLib)
    poa_diffuse = haydavies(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        dhi=data.data['Gd(h)'],
        dni=data.data['Gb(n)'],
        dni_extra=extra_radiation,
        solar_zenith=solar_position.apparent_zenith,
        solar_azimuth=solar_position.azimuth
    )

    # Ground Diffuse radiation (From PvLib)
    poa_ground = get_ground_diffuse(
        data.latitude,
        data.data['G(h)'],
        surface_type='urban'
    )

    # Angle of incidence at best orientation
    _aoi = aoi(
        surface_tilt=surface_tilt,
        surface_azimuth=surface_azimuth,
        solar_zenith=solar_position.apparent_zenith,
        solar_azimuth=solar_position.apparent_zenith
    )

    # Total radiation at plane of the pv array.
    poa_total = poa_components(
        aoi=_aoi,
        dni=data.data['Gb(n)'],
        poa_sky_diffuse=poa_diffuse,
        poa_ground_diffuse=poa_ground
    )

    return poa_total, _aoi


def _surface_tilt(latitude):
    """
    Returns the best surface tilt.
    Equation by Oxford model.
    Reference: 
    """

    lat = latitude

    # In north hemisphere
    if lat > 0:
        best_tilt = 1.3793 + lat * \
            (1.2011 + lat*(-0.014404 + lat*(0.000080509)))

    # In south hemisphere
    elif lat < 0:
        best_tilt = -0.41657 + lat * \
            (1.4216 + lat*(0.024051 + lat*(0.00021828)))

    # In the equator
    else:
        best_tilt = 0

    return best_tilt


def _surface_azimuth(latitude):
    """
    Returns the best surface azimuth.
    South (180°) for north hemisphere,
    North (0°) for south hemisphere.
    """

    if latitude > 0:
        surface_azimuth = 180
    else:
        surface_azimuth = 0

    return surface_azimuth
