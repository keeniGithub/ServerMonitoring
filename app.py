import subprocess
import time
from flask import Flask, jsonify, render_template, Response
import psutil

app = Flask(__name__)

def get_cpu_temperature():
    try:
        # Выполняем команду `sensors` и получаем вывод
        output = subprocess.check_output(['sensors']).decode('utf-8')
        # Ищем строку с температурой процессора
        for line in output.splitlines():
            if 'Core' in line:  # Обычно температура процессора начинается со слова "Core"
                # Извлекаем температуру из строки
                parts = line.split()
                # Предполагаем, что температура будет в формате 'xx.x°C'
                temp = parts[2]  # Обычно температура находится на третьей позиции
                return temp
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/cpu_percent", methods=["GET"])
def cpu_percent():
    return jsonify(cpu_percent=psutil.cpu_percent(interval=1))

@app.route('/cpu_temperature', methods=['GET'])
def cpu_temperature():
    temperature = get_cpu_temperature()
    return jsonify(cpu_temp=temperature)

@app.route("/ram_stats", methods=["GET"])
def ram_stats():
    memory_info = psutil.virtual_memory()
    total_memory_gb = memory_info.total / (1024 ** 3)
    used_memory_gb = memory_info.used / (1024 ** 3)
    memory_perecent = memory_info.percent
    return jsonify(ram_use=f"{used_memory_gb:.2f} Гб / {total_memory_gb:.2f} Гб | {memory_perecent}%")

@app.route("/network_speed", methods=["GET"])
def network_speed():
    net_io_start = psutil.net_io_counters()
    time.sleep(1)  # Ждем 1 секунду для измерения
    net_io_end = psutil.net_io_counters()

    # Вычисляем разницу в байтах
    bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
    bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv

    # Переводим байты в мегабиты и округляем до сотых
    mb_sent = round((bytes_sent * 8) / (1024 * 1024), 2)
    mb_recv = round((bytes_recv * 8) / (1024 * 1024), 2)

    return jsonify(sent=mb_sent, recv=mb_recv)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
