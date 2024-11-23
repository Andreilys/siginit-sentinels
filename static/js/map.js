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
            <div class="intel-popup">
                <h5 class="popup-title">${point.title}</h5>
                <div class="popup-content">
                    <p><strong>Source:</strong> ${point.source}</p>
                    <p><strong>Time:</strong> ${new Date(point.timestamp).toLocaleDateString(undefined, {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    })}</p>
                    <p><strong>Priority:</strong> ${point.priority}</p>
                    <p><strong>Credibility Score:</strong> ${point.credibility_score.toFixed(2)}</p>
                    <p><strong>Content Preview:</strong></p>
                    <div class="content-preview">${point.content ? point.content.substring(0, 150) + '...' : 'No content available'}</div>
                </div>
            </div>
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
