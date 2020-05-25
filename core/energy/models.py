"""Models for energy calculation."""

# PvLib
from pvlib.iotools.pvgis import get_pvgis_tmy
from pvlib.pvsystem import retrieve_sam

# Utiltites
import pandas as pd
from requests import HTTPError
from timezonefinder import TimezoneFinder


# Models
class PvgisRequest:
    """
    Class to get climatological and solar data
    from PvGis API.
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = None
        self.timezone = None
        self.data = None
        self.error_pvgis_request = None

    def get(self):
        try:
            # Request to PvGIS API.
            pvg = get_pvgis_tmy(
                lat=self.latitude,
                lon=self.longitude
            )
        except Exception:
            # Rquest to a secure place
            pvg = get_pvgis_tmy(lat=19, lon=-100)
            self.error_pvgis_request = True

        # Get only util data.
        self.data = pvg[0]
        self.data_tmy_manage()
        self.elevation = pvg[2]['location']['elevation']

        return self

    def data_tmy_manage(self):
        # Find the local time zone
        tf = TimezoneFinder()
        self.timezone = tf.timezone_at(
            lng=self.longitude,
            lat=self.latitude
        )

        # Convert UTC time to local time
        self.data.index = self.data.index.tz_convert(self.timezone)
        self.data.index.name = f'{self.timezone}'


class Module:
    """
    Class to manage pv module info.
    """

    def __init__(self):
        self.modules = retrieve_sam(name='SandiaMod')
        self.module = None

    def get_propertys(self, module_name):
        # Adquire module info from Retriev Sam database
        self.module = module_name
        self.propertys = self.modules[module_name]


class Inverter:
    """
    Class to manage pv module info.
    """

    def __init__(self):
        self.inverters = retrieve_sam(name='SandiaInverter')
        self.inverter = None

    def get_propertys(self, inverter_name):
        # Adquire module info from Retriev Sam database
        self.inverter = inverter_name
        self.propertys = self.inverters[inverter_name]
