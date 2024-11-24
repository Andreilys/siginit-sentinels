let map;
let markers = [];

let heatLayer;
let markerLayer;
let currentView = 'markers';

function initMap() {
    map = L.map('map').setView([50.4501, 30.5234], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    markerLayer = L.layerGroup().addTo(map);
    
    // Load initial intel points and set up filters
    loadIntelPoints();
    setupFilters();
    setupViewControls();
}

function setupViewControls() {
    document.querySelectorAll('[data-view]').forEach(button => {
        button.addEventListener('click', function() {
            const view = this.dataset.view;
            
            // Update active button
            document.querySelectorAll('[data-view]').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            // Switch view
            currentView = view;
            updateVisualization();
        });
    });
}

function updateVisualization() {
    if (currentView === 'heatmap') {
        markerLayer.clearLayers();
        initHeatmap(window.intelData);
    } else {
        if (heatLayer) {
            map.removeLayer(heatLayer);
        }
        loadIntelPoints();
    }
}

function initHeatmap(data) {
    if (heatLayer) {
        map.removeLayer(heatLayer);
    }
    
    const heatData = data.map(point => [
        point.latitude,
        point.longitude,
        calculateIntensity(point)
    ]);
    
    heatLayer = L.heatLayer(heatData, {
        radius: 25,
        blur: 15,
        maxZoom: 10,
        gradient: {
            0.4: '#ffffb2',
            0.6: '#fd8d3c',
            0.8: '#f03b20',
            1.0: '#bd0026'
        }
    }).addTo(map);
}

function calculateIntensity(point) {
    // Calculate intensity based on priority and credibility
    return (point.priority === 1 ? 1.0 : 
            point.priority === 2 ? 0.7 : 
            0.4) * point.credibility_score;
}

function getPriorityColor(priority) {
    switch(priority) {
        case 1:
            return '#ff0000';  // High priority - Red
        case 2:
            return '#ffa500';  // Medium priority - Orange
        case 3:
            return '#ffff00';  // Low priority - Yellow
        default:
            return '#808080';  // Unknown - Gray
    }
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
            window.intelData = data;
            if (currentView === 'markers') {
                clearMapMarkers();
                data.forEach(point => addMarker(point));
            } else {
                initHeatmap(data);
            }
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

// Initialize map and socket handlers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize map
    initMap();
    
    // Set up socket event handlers if socket is available
    if (window.socket) {
        window.socket.on('intel_update', function(data) {
            if (data.coordinates) {
                updateMap(data.coordinates);
            }
        });
    }
});
