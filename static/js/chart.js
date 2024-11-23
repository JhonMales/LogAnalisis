document.addEventListener("DOMContentLoaded", function () {
    // Gráfico de tipos de logs
    const logTypeCtx = document.getElementById('logTypeChart').getContext('2d');
    const logTypeChart = new Chart(logTypeCtx, {
        type: 'pie',
        data: {
            labels: ['Error', 'Advertencia', 'Información'],
            datasets: [{
                data: [logData.error_logs, logData.warning_logs, logData.info_logs],
                backgroundColor: ['#ff6384', '#ffce56', '#36a2eb'],
                borderWidth: 1
            }]
        }
    });

    // Gráfico de conteo diario de logs
    const dailyLogCtx = document.getElementById('dailyLogChart').getContext('2d');
    const dailyLogChart = new Chart(dailyLogCtx, {
        type: 'line',
        data: {
            labels: Object.keys(logData.daily_log_counts),
            datasets: [{
                label: 'Conteo Diario de Logs',
                data: Object.values(logData.daily_log_counts),
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});
