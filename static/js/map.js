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

function getPriorityColor(priority) {
    return priority === 1 ? 'red' :
           priority === 2 ? 'orange' :
           'yellow';
}

function addMarker(point) {
    const markerIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: ${getPriorityColor(point.priority)}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>`,
        iconSize: [12, 12]
    });

    const marker = L.marker([point.latitude, point.longitude], { icon: markerIcon })
        .bindPopup(`
            <div class="intel-popup">
                <h5 class="popup-title">${point.title}</h5>
                <div class="popup-content">
                    <p><strong>Intelligence Type:</strong> ${point.intel_type}</p>
                    <p><strong>Subtype:</strong> ${point.intel_subtype}</p>
                    <p><strong>Source Reliability:</strong> ${point.source_reliability}</p>
                    <p><strong>Information Credibility:</strong> ${point.info_credibility}</p>
                    <p><strong>Priority Level:</strong> ${point.priority}</p>
                    <p><strong>Time:</strong> ${new Date(point.timestamp).toLocaleDateString()}</p>
                    <div class="content-preview">${point.content || 'No content available'}</div>
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
    const applyButton = document.getElementById('apply-filters');
    
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
    });

    applyButton.addEventListener('click', filterIntelPoints);
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
