document.body.style.zoom = 0.25 

function updateSystemStats() {
    fetch('/system_stats')
        .then(response => response.json())
        .then(data => {
            const cpuPercent = data.cpu_percent 
            const cpuTemp = parseFloat(data.cpu_temp)
            const ramUsed = data.ram_stats.used 
            const ramTotal = data.ram_stats.total 
            const ramPercent = data.ram_stats.percent 

            document.getElementById('cpu-percent').innerText = cpuPercent + '%' 
            document.getElementById('cpu-temperature').innerText = cpuTemp 
            document.getElementById('ram-used').innerText = ramUsed.toFixed(2) 
            document.getElementById('ram-total').innerText = ramTotal.toFixed(2) 
            document.getElementById('ram-percent').innerText = ramPercent 

            const cpuTempElement = document.getElementById('cpu-temperature') 
            const ramUsedElement = document.getElementById('ram-used') 
            const cpuPercentElement = document.getElementById('cpu-percent') 

            if (cpuTemp > 70) {
                cpuTempElement.classList.add('alert') 
            } else {
                cpuTempElement.classList.remove('alert') 
            }

            if (ramPercent > 80) {
                ramUsedElement.classList.add('alert') 
            } else {
                ramUsedElement.classList.remove('alert') 
            }

            if (cpuPercent > 80) {
                cpuPercentElement.classList.add('alert') 
            } else {
                cpuPercentElement.classList.remove('alert') 
            }
        })
        .catch(error => console.error('Error fetching system stats:', error)) 
}

function updateNetStats() {
    fetch('/network_speed')
        .then(response => response.json())
        .then(data => {
            document.getElementById('sent').innerText = data.sent 
            document.getElementById('recv').innerText = data.recv 
        })
        .catch(error => console.error('Error fetching network stats:', error)) 
}

setInterval(updateSystemStats, 1000)
setInterval(updateNetStats, 1000)
