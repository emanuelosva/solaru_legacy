<img src="app/static/img/favicon.png" width="200" >

# Solaru App
Solaru App es una aplicación web escrita en Python, pensada para calcular un sistema fotovoltáico diseñado específicamente a las condiciones de tu hogar ☀.
Para ello solo necesitas ingresas tu ubicación (latitud y longitud), el espacio disponible, tu consumo promedio de energía y el costo del kWh para realizar el análisis económico.

## Tecnologías
| Backend  |  Frontend  |
| ------------ | ------------ |
|  [Flask](https://flask.palletsprojects.com/en/1.1.x/ "Flask")  |  HTML  |
|  [PvLib](https://pvlib-python.readthedocs.io/en/stable/ "PvLib") |  CSS  |
|  [PVGIS](https://ec.europa.eu/jrc/en/PVGIS/releases/pvgis51 "PVGIS") |  [Bootstrap](https://getbootstrap.com/ "Bootstrap")  |

## Estructura
Solaru app se encuentra dividida en dos módulos principales:
*   Módulo **App**: Maneja la lógica para crear la app y renderear las vistas.

*   Módulo **Core**: Maneja toda la lógica de los cálculos necesarios. A su vez se encuentra dividido en:
    -   **enviroment**: Determina el impacto ambiental positivo derivado del sistema fotovoltaico.
    -   **energy**: Que hace uso de la librería [PvLib](https://pvlib-python.readthedocs.io/en/stable/ "PvLib") para conectarse a la API de PVGIS y disponer de los datos climatológicos y solares necesarios. Además, se implementan una serie de funciones que determinan el tamaño del sistema y la energía que este podría producir.
    -   **financial**: Aquí se realizan los cálculos que determinan el beneficio económico y el costo del sistema.


> Todos los cálculos se basan en métodos provistos por:
> * El [NREL](https://www.nrel.gov/research/re-solar.html "NREL") (National Renewable Energy Laboratory)
> * [PvPerformance](https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/ "PvPErformance") 


## Pruébala ahora
La aplicación la puedes consultar [aquí](https://solaru.ue.r.appspot.com/ "aquí") ya!

## Preview
<img src="app/static/img/preview.PNG" width="600px">

### Notas
Si el tema te gusta y quieres contribuir para convertir este proyecto en algo más grande, clonalo y ponte en contacto conmigo 😎.
