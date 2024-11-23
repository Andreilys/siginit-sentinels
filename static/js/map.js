let map;
let markers = [];

function initMap() {
    map = L.map('map').setView([50.4501, 30.5234], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Load initial intel points
    fetch('/api/intel-points')
        .then(response => response.json())
        .then(data => {
            data.forEach(point => addMarker(point));
        });
}

function addMarker(point) {
    const marker = L.marker([point.latitude, point.longitude])
        .bindPopup(`
            <strong>${point.title}</strong><br>
            Priority: ${point.priority}<br>
            Time: ${new Date(point.timestamp).toLocaleString()}
        `);
    
    markers.push(marker);
    marker.addTo(map);
}

function updateMap(coordinates) {
    addMarker({
        latitude: coordinates.lat,
        longitude: coordinates.lng,
        title: coordinates.title,
        priority: coordinates.priority,
        timestamp: new Date()
    });
}

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', initMap);
