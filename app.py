from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

# Flask Application
app = Flask(__name__)

# โหลด YOLO Model
model = YOLO('yolov8n.pt')

# ตัวแปรควบคุมสถานะกล้อง
camera = None  # ตัวแปรสำหรับเก็บกล้อง

# Route แสดงหน้าเว็บ
@app.route('/')
def index():
    return render_template('index.html')

# Route เปิดกล้อง
@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)  # เปิดกล้อง
        if not camera.isOpened():
            camera = None
            return jsonify({'message': 'Failed to open camera'}), 500

        while True:
            ret, frame = camera.read()
            if not ret:
                break

            # ตรวจจับวัตถุ
            results = model(frame)
            annotated_frame = results[0].plot()

            # แสดงผลลัพธ์
            cv2.imshow('Detection', annotated_frame)

            # กด 'q' เพื่อหยุด
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()
        camera = None
        return jsonify({'message': 'Camera stopped'}), 200

    return jsonify({'message': 'Camera is already running'}), 200

# Route ปิดกล้อง
@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera
    if camera is not None:
        camera.release()  # ปิดกล้อง
        cv2.destroyAllWindows()
        camera = None
        return jsonify({'message': 'Camera stopped'}), 200
    return jsonify({'message': 'Camera is not running'}), 200


if __name__ == '__main__':
    app.run(debug=True)