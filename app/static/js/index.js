// Pricipal DOM elements
const geoLoc = document.getElementById('geoloc')
const ouput = document.getElementById('out')
const inLatitude = document.getElementById('latitude')
const inLongitude = document.getElementById('longitude')

// Auxiliar functions
const success = (location) => {
    // Get coordinates
    const latitude = location.coords.latitude
    const longitude = location.coords.longitude
    // Insert in inputs
    inLatitude.value = latitude
    inLongitude.value = longitude
    // Success message
    geoLoc.innerHTML = '✔'
}

const error = () => {
    geoLoc.innerHTML = '❗'
    ouput.innerHTML = 'Hubo un error al buscar tu ubicación. (Puedes escribirla a mano)'
}

const geoFindMe = () => {
    // Check if gelocation is disponible
    if (!navigator.geolocation) {
        geoLoc.innerHTML = '❗'
        ouput.innerHTML = 'Tu navegador no soporta la geolocalización'
    }

    geoLoc.innerHTML = 'Loading...'
    // Get position
    navigator.geolocation.getCurrentPosition(success, error)
}