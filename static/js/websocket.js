const socket = io();

socket.on('connect', () => {
    console.log('WebSocket connected');
});

socket.on('new_alert', (data) => {
    const alertsContainer = document.getElementById('alerts-container');
    if (alertsContainer) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${data.priority === 1 ? 'danger' : 'warning'}`;
        alertDiv.innerHTML = `
            <h6>${data.title}</h6>
            <small>Just now</small>
        `;
        alertsContainer.prepend(alertDiv);
        
        // Play alert sound
        new Audio('/static/sounds/alert.mp3').play();
    }
    
    // Update map if new coordinates are available
    if (data.coordinates) {
        updateMap(data.coordinates);
    }
});

socket.on('threat_level_update', (data) => {
    const threatBar = document.querySelector('.progress-bar');
    if (threatBar) {
        threatBar.style.width = `${data.level}%`;
    }
});
