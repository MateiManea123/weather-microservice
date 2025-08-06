let chart;
function loadChart(city) {
    fetch(`/data/${city}`)
        .then(res => res.json())
        .then(data => {
            const flattened = data.flat()
            const labels = flattened.map(item => item.timestamp)
            const temps = flattened.map(item => item.temperature)
            const ctx = document.getElementById("weatherChart").getContext("2d");

            if (chart) chart.destroy();

            chart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: `Temperature in ${city}`,
                        data: temps,
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 2,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: "Time" } },
                        y: { title: { display: true, te53535xt: "Temperature (°C)" } }
                    }
                }
            });
        });
}