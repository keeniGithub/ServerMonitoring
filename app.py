import time
from flask import Flask, jsonify, render_template, Response
import cv2
import numpy as np
import psutil
import pyautogui
import os
from PIL import Image

app = Flask(__name__)

def generate_frames():
    img_path = "Z:\script\JS\Monitoring\static\cursor.png" if os.name == 'nt' else "/home/kenyka/Documents/GitHub/ServerMonitoring/static/cursor.png"
    cursor_image = Image.open(img_path)
    cursor_width, cursor_height = 16, 16

    while True:
        # Захват экрана
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        # Получаем позицию курсора
        cursor_x, cursor_y = pyautogui.position()

        # Преобразование цвета от RGB к BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Накладываем курсор на изображение
        screenshot_pil = Image.fromarray(frame)
        screenshot_pil.paste(cursor_image, (cursor_x - cursor_width // 2, cursor_y - cursor_height // 2), cursor_image)

        # Преобразуем обратно в массив NumPy
        frame_with_cursor = np.array(screenshot_pil)

        # Кодирование в JPEG
        ret, buffer = cv2.imencode('.jpg', frame_with_cursor)
        frame_with_cursor = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_with_cursor + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cpu_percent", methods=["GET"])
def cpu_percent():
    return jsonify(cpu_percent=psutil.cpu_percent(interval=1))

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
