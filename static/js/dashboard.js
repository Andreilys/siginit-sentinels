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

    // Initialize timeline
    initTimeline();
}

function initRealTimeUpdates() {
    // Set up WebSocket listeners for real-time updates
    if (window.socket) {
        window.socket.on('intel_update', function(data) {
            updateMap(data.coordinates);
            updateThreatLevel();
            updateStatistics();
        });
        
        window.socket.on('alert_update', function(data) {
            updateAlerts(data);
        });
    }
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
            // Update priority counts
            document.getElementById('high-priority-count').textContent = data.highPriority;
            document.getElementById('medium-priority-count').textContent = data.mediumPriority;
            document.getElementById('low-priority-count').textContent = data.lowPriority;
            
            // Update intel type breakdown
            const breakdownDiv = document.getElementById('intel-type-breakdown');
            breakdownDiv.innerHTML = ''; // Clear existing content
            
            Object.entries(data.intelTypes).forEach(([type, info]) => {
                const typeDiv = document.createElement('div');
                typeDiv.className = 'mb-3';
                
                // Add type header with total count
                typeDiv.innerHTML = `
                    <div class="d-flex justify-content-between mb-2">
                        <span class="fw-bold">${type}:</span>
                        <span class="badge bg-primary">${info.total}</span>
                    </div>
                `;
                
                // Add subtypes
                const subtypesDiv = document.createElement('div');
                subtypesDiv.className = 'ms-3';
                Object.entries(info.subtypes).forEach(([subtype, count]) => {
                    subtypesDiv.innerHTML += `
                        <div class="d-flex justify-content-between mb-1">
                            <span class="small">${subtype}:</span>
                            <span class="badge bg-secondary">${count}</span>
                        </div>
                    `;
                });
                typeDiv.appendChild(subtypesDiv);
                breakdownDiv.appendChild(typeDiv);
            });
            
            // Add reliability distribution
            const reliabilityDiv = document.createElement('div');
            reliabilityDiv.className = 'mt-3';
            reliabilityDiv.innerHTML = `
                <h6>Source Reliability</h6>
                ${Object.entries(data.sourceReliability).map(([level, count]) => `
                    <div class="d-flex justify-content-between mb-1">
                        <span>Level ${level}:</span>
                        <span class="badge bg-info">${count}</span>
                    </div>
                `).join('')}
            `;
            breakdownDiv.appendChild(reliabilityDiv);
            
            // Add credibility distribution
            const credibilityDiv = document.createElement('div');
            credibilityDiv.className = 'mt-3';
            credibilityDiv.innerHTML = `
                <h6>Information Credibility</h6>
                ${Object.entries(data.infoCredibility).map(([level, count]) => `
                    <div class="d-flex justify-content-between mb-1">
                        <span>Level ${level}:</span>
                        <span class="badge bg-info">${count}</span>
                    </div>
                `).join('')}
            `;
            breakdownDiv.appendChild(credibilityDiv);
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

// Timeline functionality
function initTimeline() {
    fetch('/api/intel-points')
        .then(response => response.json())
        .then(data => {
            window.intelData = data;
            initializeTimeline();
        });
}

function initializeTimeline(startDate = null, endDate = null) {
    const timelineData = [];
    const timelineDates = {};
    
    // Filter data based on date range
    const filteredData = startDate && endDate ? 
        intelData.filter(item => {
            const date = new Date(item.timestamp);
            return date >= startDate && date <= endDate;
        }) : intelData;
    
    // Process intelligence data into timeline format
    filteredData.forEach(item => {
        const date = new Date(item.timestamp).toISOString().split('T')[0];
        if (!timelineDates[date]) {
            timelineDates[date] = 0;
        }
        timelineDates[date]++;
    });
    
    // Convert to array format for visualization
    Object.keys(timelineDates).sort().forEach(date => {
        timelineData.push({
            date: date,
            count: timelineDates[date]
        });
    });
    
    // Clear existing timeline
    document.getElementById('intelligence-timeline').innerHTML = '';
    
    // Create timeline chart using D3.js
    const margin = {top: 20, right: 20, bottom: 30, left: 40};
    const width = document.getElementById('intelligence-timeline').offsetWidth - margin.left - margin.right;
    const height = 200 - margin.top - margin.bottom;
    
    const svg = d3.select('#intelligence-timeline')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
        
    // Add X axis
    const x = d3.scaleTime()
        .domain(d3.extent(timelineData, d => new Date(d.date)))
        .range([0, width]);
    
    svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));
        
    // Add Y axis
    const y = d3.scaleLinear()
        .domain([0, d3.max(timelineData, d => d.count)])
        .range([height, 0]);
        
    svg.append('g')
        .call(d3.axisLeft(y));
        
    // Add the bars
    svg.selectAll('rect')
        .data(timelineData)
        .enter()
        .append('rect')
        .attr('x', d => x(new Date(d.date)))
        .attr('y', d => y(d.count))
        .attr('width', width / timelineData.length - 1)
        .attr('height', d => height - y(d.count))
        .attr('fill', '#4a90e2');
}

function refreshTimeline() {
    fetch('/api/intel-points')
        .then(response => response.json())
        .then(data => {
            window.intelData = data;
            initializeTimeline();
        });
}

// Add event listeners for timeline controls
document.addEventListener('DOMContentLoaded', function() {
    // Quick filter buttons
    document.querySelectorAll('[data-timerange]').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            document.querySelectorAll('[data-timerange]').forEach(btn => {
                btn.classList.remove('active');
            });
            // Add active class to clicked button
            this.classList.add('active');
            
            const range = this.dataset.timerange;
            const now = new Date();
            let startDate = new Date();
            const endDate = document.getElementById('end-date');
            const startDatePicker = document.getElementById('start-date');
            
            // Always set end date to today
            const today = new Date().toISOString().split('T')[0];
            endDate.value = today;
            
            switch(range) {
                case 'today':
                    startDate = new Date(now.setHours(0,0,0,0));
                    break;
                case 'week':
                    startDate.setDate(startDate.getDate() - 7);
                    break;
                case 'month':
                    startDate.setMonth(startDate.getMonth() - 1);
                    break;
            }
            
            // Update date picker values
            startDatePicker.value = startDate.toISOString().split('T')[0];
            
            // Update timeline
            initializeTimeline(startDate, new Date());
        });
    });
    
    // Custom date range filter
    document.getElementById('apply-date-filter').addEventListener('click', function() {
        const startDate = new Date(document.getElementById('timeline-start-date').value);
        const endDate = new Date(document.getElementById('timeline-end-date').value);
        
        if (!isNaN(startDate.getTime()) && !isNaN(endDate.getTime())) {
            initializeTimeline(startDate, endDate);
        }
    });

    const zoomIn = document.getElementById('timeline-zoom-in');
    const zoomOut = document.getElementById('timeline-zoom-out');
    const refresh = document.getElementById('timeline-refresh');
    const play = document.getElementById('timeline-play');

    if (zoomIn) zoomIn.addEventListener('click', () => {
        // Implement zoom in functionality
    });

    if (zoomOut) zoomOut.addEventListener('click', () => {
        // Implement zoom out functionality
    });

    if (refresh) refresh.addEventListener('click', refreshTimeline);

    if (play) play.addEventListener('click', () => {
        // Implement play/pause functionality
    });
});

function updateTimeline(events) {
    const timelineContainer = document.getElementById('intel-timeline');
    if (!timelineContainer) return;

    const timelineHtml = events.map(event => `
        <div class="timeline-item list-group-item list-group-item-action">
            <div class="d-flex w-100 justify-content-between">
                <h6 class="mb-1">${event.source}</h6>
                <small class="text-muted">${formatDate(event.timestamp)}</small>
            </div>
            <p class="mb-1">${event.content ? event.content.substring(0, 150) + '...' : 'No content available'}</p>
            <small class="text-muted">
                Priority: ${getPriorityBadge(event.priority)} | 
                Credibility: ${event.credibility_score.toFixed(2)}
            </small>
        </div>
    `).join('');

    timelineContainer.innerHTML = timelineHtml;
}

function formatDate(timestamp) {
    const date = new Date(timestamp);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

function getPriorityBadge(priority) {
    const classes = {
        1: 'danger',
        2: 'warning',
        3: 'info'
    };
    return `<span class="badge bg-${classes[priority] || 'secondary'}">${priority}</span>`;
}

// Socket.IO event handler for timeline updates
// Socket.IO event handler for timeline updates
if (window.socket) {
    window.socket.on('intel_update', function(data) {
        initTimeline(); // Refresh timeline with new data
    });
}

// Set default dates in date inputs
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    if (startDate && endDate) {
        endDate.value = today.toISOString().split('T')[0];
        today.setDate(today.getDate() - 30); // Default to last 30 days
        startDate.value = today.toISOString().split('T')[0];
    }
});

// Make functions available globally
window.dashboardUtils = {
    updateThreatLevel,
    updateStatistics,
    updateAlerts,
    initTimeline
};
