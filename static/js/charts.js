function renderAdminCharts(occupancyLabels, occupiedData, availableData, revenueLabels, revenueData) {
    const ctx1 = document.getElementById('occupancyChart');
    if (ctx1) {
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: occupancyLabels,
                datasets: [
                    {
                        label: 'Occupied',
                        data: occupiedData
                    },
                    {
                        label: 'Available',
                        data: availableData
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    const ctx2 = document.getElementById('revenueChart');
    if (ctx2) {
        new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: revenueLabels,
                datasets: [
                    {
                        label: 'Revenue',
                        data: revenueData
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

function renderUserChart(labels, values) {
    const ctx = document.getElementById('userHistoryChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Total Spend',
                        data: values
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}