// Dashboard initialization and real-time updates
document.addEventListener('DOMContentLoaded', function() {
    initDashboard();
    initRealTimeUpdates();
});

function initDashboard() {
    // Initialize threat level indicator
    updateThreatLevel();
    
    // Initialize statistics counters
    updateStatistics();
    
    // Set up alert notifications
    setupNotifications();
}

function initRealTimeUpdates() {
    // Set up WebSocket listeners for real-time updates
    socket.on('intel_update', function(data) {
        updateMap(data.coordinates);
        updateThreatLevel();
        updateStatistics();
    });
    
    socket.on('alert_update', function(data) {
        updateAlerts(data);
    });
}

function updateThreatLevel() {
    fetch('/api/threat-level')
        .then(response => response.json())
        .then(data => {
            const threatBar = document.querySelector('.progress-bar');
            if (threatBar) {
                threatBar.style.width = `${data.level}%`;
                threatBar.setAttribute('aria-valuenow', data.level);
                
                // Update threat level color based on severity
                threatBar.className = 'progress-bar';
                if (data.level > 75) {
                    threatBar.classList.add('bg-danger');
                } else if (data.level > 50) {
                    threatBar.classList.add('bg-warning');
                } else {
                    threatBar.classList.add('bg-info');
                }
            }
        });
}

function updateStatistics() {
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            // Update active incidents count
            const incidentsElement = document.getElementById('active-incidents');
            if (incidentsElement) {
                incidentsElement.textContent = data.activeIncidents;
            }
            
            // Update other statistics
            updateStatisticElement('high-priority-count', data.highPriority);
            updateStatisticElement('medium-priority-count', data.mediumPriority);
            updateStatisticElement('low-priority-count', data.lowPriority);
        });
}

function updateStatisticElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

function updateAlerts(data) {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    
    // Create new alert element
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${getPriorityClass(data.priority)} alert-dismissible fade show`;
    alertElement.innerHTML = `
        <strong>${data.title}</strong>
        <p class="mb-0">${data.description}</p>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to container
    alertsContainer.insertBefore(alertElement, alertsContainer.firstChild);
    
    // Remove old alerts if too many
    while (alertsContainer.children.length > 10) {
        alertsContainer.removeChild(alertsContainer.lastChild);
    }
    
    // Trigger notification
    if (Notification.permission === "granted") {
        new Notification("New Intelligence Alert", {
            body: data.title,
            icon: "/static/images/alert-icon.png"
        });
    }
}

function getPriorityClass(priority) {
    switch (priority) {
        case 1: return 'danger';
        case 2: return 'warning';
        default: return 'info';
    }
}

function setupNotifications() {
    if ("Notification" in window) {
        Notification.requestPermission();
    }
}

// Export functions for use in other modules
export {
    updateThreatLevel,
    updateStatistics,
    updateAlerts
};
