let map;
let markers = [];

function initMap() {
    map = L.map('map').setView([50.4501, 30.5234], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Load initial intel points and set up filters
    loadIntelPoints();
    setupFilters();
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

function loadIntelPoints() {
    fetch('/api/intel-points')
        .then(response => response.json())
        .then(data => {
            clearMapMarkers();
            data.forEach(point => addMarker(point));
        });
}

function clearMapMarkers() {
    markers.forEach(marker => marker.remove());
    markers = [];
}

function setupFilters() {
    const typeSelect = document.getElementById('intel-type-filter');
    const subtypeSelect = document.getElementById('intel-subtype-filter');
    
    // Disable subtype initially
    subtypeSelect.disabled = true;
    
    typeSelect.addEventListener('change', function(e) {
        const selectedType = e.target.value;
        subtypeSelect.innerHTML = '<option value="">All Subtypes</option>';
        subtypeSelect.disabled = !selectedType;
        
        if (selectedType) {
            const subtypes = {
                'IMINT': ['Satellite imagery', 'Drone surveillance', 'Aerial photography', 'Ground-based photography'],
                'SIGINT': ['Radio intercepts', 'Communications monitoring', 'Electronic signals', 'Encryption analysis'],
                'HUMINT': ['Spies and covert operatives', 'Informants', 'Diplomatic sources', 'Prisoner interrogations'],
                'OSINT': ['Social media monitoring', 'News media and publications', 'Academic research', 'Public forums and websites'],
                'CYBERINT': ['Malware analysis', 'Dark web monitoring', 'Network traffic analysis', 'Threat intelligence feeds']
            };
            
            subtypes[selectedType].forEach(subtype => {
                const option = document.createElement('option');
                option.value = subtype;
                option.textContent = subtype;
                subtypeSelect.appendChild(option);
            });
        }
        
        filterIntelPoints();
    });

    // Add event listeners for other filters
    document.getElementById('intel-subtype-filter').addEventListener('change', filterIntelPoints);
    document.getElementById('source-reliability-filter').addEventListener('change', filterIntelPoints);
    document.getElementById('info-credibility-filter').addEventListener('change', filterIntelPoints);
}

function filterIntelPoints() {
    const filters = {
        type: document.getElementById('intel-type-filter').value,
        subtype: document.getElementById('intel-subtype-filter').value,
        reliability: document.getElementById('source-reliability-filter').value,
        credibility: document.getElementById('info-credibility-filter').value
    };
    
    fetch('/api/intel-points?' + new URLSearchParams(filters))
        .then(response => response.json())
        .then(data => {
            clearMapMarkers();
            data.forEach(point => addMarker(point));
        });
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
