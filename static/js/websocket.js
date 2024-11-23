// Initialize Socket.IO with reconnection options
const socket = io({
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    timeout: 20000
});

// Connection event handlers
socket.on('connect', () => {
    console.log('WebSocket connected');
    // Remove any existing connection error messages
    const errorElement = document.getElementById('socket-error');
    if (errorElement) {
        errorElement.remove();
    }
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    showConnectionError();
});

socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
    if (reason === 'io server disconnect') {
        // Reconnect manually if server disconnected
        socket.connect();
    }
});

socket.on('reconnect_attempt', (attemptNumber) => {
    console.log(`Attempting to reconnect... (${attemptNumber})`);
});

// Alert handling
socket.on('new_alert', (data) => {
    const alertsContainer = document.getElementById('alerts-container');
    if (alertsContainer) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${data.priority === 1 ? 'danger' : 'warning'}`;
        alertDiv.innerHTML = `
            <h6>${data.title}</h6>
            <small>Just now</small>
            <button type="button" class="btn btn-sm btn-outline-secondary ms-2" onclick="playAlertSound()">
                Play Sound
            </button>
        `;
        alertsContainer.prepend(alertDiv);
        
        // Update map if new coordinates are available
        if (data.coordinates) {
            updateMap(data.coordinates);
        }
    }
});

socket.on('threat_level_update', (data) => {
    const threatBar = document.querySelector('.progress-bar');
    if (threatBar) {
        threatBar.style.width = `${data.level}%`;
    }
});

// Helper functions
function showConnectionError() {
    // Only show error if it doesn't already exist
    if (!document.getElementById('socket-error')) {
        const errorDiv = document.createElement('div');
        errorDiv.id = 'socket-error';
        errorDiv.className = 'alert alert-warning alert-dismissible fade show';
        errorDiv.innerHTML = `
            <strong>Connection Error</strong>: Unable to connect to the server. 
            Attempting to reconnect...
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container').insertBefore(errorDiv, document.querySelector('.container').firstChild);
    }
}

function playAlertSound() {
    const audio = new Audio('/static/sounds/alert.mp3');
    audio.play().catch(error => {
        console.error('Error playing sound:', error);
    });
}
