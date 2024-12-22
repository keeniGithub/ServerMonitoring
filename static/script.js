document.body.style.zoom = 0.25;
console.log("wefwef")

function updateCpuPercent() {
    fetch('/cpu_percent')
        .then(response => response.json())
        .then(data => {
            document.getElementById('cpu-percent').innerText = data.cpu_percent + '%';
        })
        .catch(error => console.error('Error fetching CPU percent:', error));
}

function updateRamStats() {
    fetch('/ram_stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('ram').innerText = data.ram_use;
        })
        .catch(error => console.error('Error fetching CPU percent:', error));
}

function updateNetStats() {
    fetch('/network_speed')
        .then(response => response.json())
        .then(data => {
            document.getElementById('sent').innerText = data.sent;
            document.getElementById('recv').innerText = data.recv;
        })
        .catch(error => console.error('Error fetching CPU percent:', error));
}

function updateCpuTemperature() {
    fetch('/cpu_temperature')
        .then(response => response.json())
        .then(data => {
            document.getElementById('cpu-temperature').innerText = data.cpu_temp;
        })
        .catch(error => console.error('Error fetching CPU percent:', error));
}

setInterval(updateCpuPercent, 1000); // Обновлять каждую секунду
setInterval(updateRamStats, 1000); // Обновлять каждую секунду
setInterval(updateNetStats, 1000); // Обновлять каждую секунду
setInterval(updateCpuTemperature, 1000); // Обновлять каждую секунду