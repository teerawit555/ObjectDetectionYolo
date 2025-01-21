# Thread Version

from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from threading import Thread

# Flask Application
app = Flask(__name__)

# โหลด YOLO Model
model = YOLO('yolov8n.pt')

# ตัวแปรควบคุมสถานะกล้อง
camera_active = False

# ฟังก์ชันสำหรับเปิดกล้อง
def start_camera_thread():
    global camera_active
    cap = cv2.VideoCapture(0)
    while camera_active:
        ret, frame = cap.read()
        if not ret:
            break
        
        # ตรวจจับวัตถุ
        results = model(frame)
        annotated_frame = results[0].plot()

        # แสดงผลลัพธ์
        cv2.imshow('Detection', annotated_frame)

        # กด 'q' เพื่อออก
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    camera_active = False

# Route แสดงหน้าเว็บ
@app.route('/')
def index():
    return render_template('index.html')

# Route ตรวจจับวัตถุจากภาพ
@app.route('/detect', methods=['POST'])
def detect():
    if 'images' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['images']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # ตรวจจับวัตถุ
    results = model(image)
    detections = [{'class': int(result[5]), 'confidence': float(result[4])} for result in results.xyxy[0]]
    return jsonify({'detections': detections})

# Route เปิดกล้อง
@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera_active
    if not camera_active:
        camera_active = True
        Thread(target=start_camera_thread).start()  # เปิดกล้องใน Thread แยก
        return jsonify({'message': 'Camera started'}), 200
    return jsonify({'message': 'Camera is already running'}), 200

# Route ปิดกล้อง
@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_active
    if camera_active:
        camera_active = False
        return jsonify({'message': 'Camera stopped'}), 200
    return jsonify({'message': 'Camera is not running'}), 200

if __name__ == '__main__':
    app.run(debug=True)

