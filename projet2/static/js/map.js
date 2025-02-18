// Initialisation de la carte
var map = L.map('map').setView([48.8566, 2.3522], 13); // Position initiale à Paris

// Ajouter un fond de carte OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Créer une couche pour gérer les marqueurs dynamiquement
var markers = L.layerGroup().addTo(map);

// Fonction pour calculer la distance entre deux points (en mètres)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371000; // Rayon de la Terre en mètres
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c; // Distance en mètres
}

// Fonction pour ajouter les marqueurs (avec filtrage par rayon de 1 km)
function addBikeMarkers(stations, userLat, userLon) {
    stations.forEach(function(station) {
        // Calculer la distance entre l'utilisateur et la station
        const distance = calculateDistance(userLat, userLon, station.latitude, station.longitude);

        // Si la station est dans un rayon de 1 km, l'ajouter à la carte
        if (distance <= 1000) {
            var marker = L.marker([station.latitude, station.longitude]);
            marker.bindPopup(
                "<b>Station : </b>" + station.commune +
                "<br><b>Places disponibles : </b>" + station.nb_places_dispo
            );
            markers.addLayer(marker); // Ajouter le marqueur à la couche
        }
    });
}

// Fonction pour charger les données des stations et mettre à jour la carte
function loadStations() {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const userLat = position.coords.latitude;
            const userLon = position.coords.longitude;

            // Récupérer les données des stations depuis l'API
            fetch('/get_stations')
                .then(response => {
                    if (!response.ok) throw new Error("Erreur réseau");
                    return response.json();
                })
                .then(data => {
                    // Nettoyer les marqueurs existants
                    markers.clearLayers();

                    // Ajouter les nouveaux marqueurs filtrés
                    addBikeMarkers(data, userLat, userLon);
                })
                .catch(error => console.error("Erreur lors de la récupération des données :", error));
        },
        function(error) {
            console.error("Erreur de géolocalisation :", error.message);
        }
    );
}

// Appeler une première fois pour charger les données
loadStations();

// Mettre à jour les stations toutes les 5 minutes
setInterval(loadStations, 300000); // 300 000 ms = 5 minutes
