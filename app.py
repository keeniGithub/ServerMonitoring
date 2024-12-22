import subprocess
import time
from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

def get_system_stats():
    # Получаем информацию о процессоре
    cpu_percent = psutil.cpu_percent(interval=1)
    temperature = get_cpu_temperature()
    
    # Получаем информацию о RAM
    memory_info = psutil.virtual_memory()
    ram_stats = {
        'total': memory_info.total / (1024 ** 3),  # в Гб
        'used': memory_info.used / (1024 ** 3),    # в Гб
        'percent': memory_info.percent
    }

    return {
        'cpu_percent': cpu_percent,
        'cpu_temp': temperature,
        'ram_stats': ram_stats
    }

def get_cpu_temperature():
    try:
        output = subprocess.check_output(['sensors']).decode('utf-8')
        for line in output.splitlines():
            if 'Core' in line:
                parts = line.split()
                temp = parts[2]
                return temp
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/system_stats", methods=["GET"])
def system_stats():
    stats = get_system_stats()
    return jsonify(stats)

@app.route("/network_speed", methods=["GET"])
def network_speed():
    net_io_start = psutil.net_io_counters()
    time.sleep(1)
    net_io_end = psutil.net_io_counters()

    bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
    bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv

    mb_sent = round((bytes_sent * 8) / (1024 * 1024), 2)
    mb_recv = round((bytes_recv * 8) / (1024 * 1024), 2)

    return jsonify(sent=mb_sent, recv=mb_recv)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
