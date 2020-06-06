// Pricipal DOM elements
const ouput = document.getElementById('out')

if (window.matchMedia('(max-width: 1023px)').matches) {
    var geoLoc = document.getElementsByName('geoloc')[1]
    var inLatitude = document.getElementsByName('latitude')[1]
    var inLongitude = document.getElementsByName('longitude')[1]
} else {
    var geoLoc = document.getElementsByName('geoloc')[0]
    var inLatitude = document.getElementsByName('latitude')[0]
    var inLongitude = document.getElementsByName('longitude')[0]
}


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