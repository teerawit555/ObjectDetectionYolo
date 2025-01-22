<a name="readme-top"></a>

<br />
<div align="center">
    <h1>Real-Time Object Detection System with YOLO Model</h1>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

โปรแกรม Object Detection with YOLO Model เป็นระบบตรวจจับวัตถุที่พัฒนาขึ้นโดยใช้ YOLOv8 Model สำหรับการตรวจจับวัตถุแบบเรียลไทม์ ระบบนี้ถูกออกแบบมาเพื่อให้ใช้งานง่ายและยืดหยุ่น 
โดยมีการผสานรวมกับ Flask API เพื่อควบคุมการทำงานผ่านเว็บอินเตอร์เฟซ พร้อมทั้งรองรับการฝึกโมเดลใหม่ด้วยชุดข้อมูลย่อยจาก COCO Dataset 

## Features

1. **Real-Time Detection** - ตรวจจับวัตถุจากกล้องแบบเรียลไทม์ พร้อมแสดงผลกรอบรอบวัตถุที่ตรวจจับได้
2. **Custom Training** - ฝึกโมเดล YOLOv8 ด้วยชุดข้อมูลย่อยจาก COCO
3. **Web Control with Flask API** - ใช้ Flask API ในการควบคุมการทำงาน เช่น การเปิด/ปิดกล้อง และการเรียกใช้งานระบบตรวจจับวัตถุ

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Installation

เพื่อติดตั้งโปรแกรม **Real-Time Object Detection System** ให้ทำตามขั้นตอนดังนี้:

1. ติดตั้ง Python [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. ติดตั้งไลบรารีที่จำเป็น
   ```sh
   pip install flask ultralytics opencv-python numpy
   ```
3. ดาวน์โหลดชุดข้อมูล COCO ย่อยจาก Kaggle
   - ชุดข้อมูล: [COCO Subset จาก Kaggle](https://www.kaggle.com/datasets/ultralytics/coco128)
   - แตกไฟล์และวางโฟลเดอร์ `train` และ `test` ไว้ในโปรเจกต์ เช่น `dl_detection/train` และ `dl_detection/test`
4. ดาวน์โหลดโมเดล YOLOv8
   - ตรวจสอบให้แน่ใจว่าไฟล์ `yolov8n.pt` อยู่ในโฟลเดอร์โปรเจกต์
   - ดาวน์โหลดได้จาก [Ultralytics YOLOv8 Repository](https://github.com/ultralytics/yolov8)
5. Clone Repository
   ```sh
   git clone https://github.com/teerawit555/ObjectDetectionYolo.git
   cd ObjectDetectionYolo
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## การฝึกโมเดล

1. สร้างไฟล์ `data.yaml` เพื่อกำหนดชุดข้อมูล
   ```yaml
   train: dl_detection/train
   val: dl_detection/test
   nc: 80
   names: [
       'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
       'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
       'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
       'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
       'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
       'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
       'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
       'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
       'scissors', 'teddy bear', 'hair drier', 'toothbrush'
   ]
   ```

2. ใช้คำสั่งนี้เพื่อเริ่มการฝึกโมเดล
   ```sh
   yolo task=detect mode=train model=yolov8n.pt data=custom_data.yaml epochs=50 imgsz=640
   ```

3. ผลลัพธ์จากการฝึกจะถูกบันทึกไว้ใน `runs/detect/train/weights` เช่นไฟล์ `best.pt`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## การใช้งานโปรแกรม

1. เริ่ม Flask Server
   ```sh
   python app.py
   ```

2. เปิดเบราว์เซอร์ไปที่
   ```
   http://127.0.0.1:5000/
   ```

3. ใช้ API Endpoints
   - **Start Camera:** เปิดกล้องและเริ่มการตรวจจับวัตถุแบบเรียลไทม์  
     ```
     POST /start_camera
     ```
     หรือกด `q` เพื่อหยุดการตรวจจับ
   - **Stop Camera:** ปิดกล้องและหยุดการตรวจจับ  
     ```
     POST /stop_camera
     ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## โครงสร้างการทำงาน

1. **Real-Time Detection**
   - เปิดกล้องและส่งภาพจากกล้องเข้าสู่โมเดล YOLOv8
   - ระบบจะแสดงกรอบรอบวัตถุที่ตรวจจับได้แบบเรียลไทม์
2. **Custom Training**
   - ฝึกโมเดล YOLOv8 ด้วยชุดข้อมูลเฉพาะ
   - ใช้ไฟล์ผลลัพธ์ (`best.pt`) ในการตรวจจับวัตถุที่ต้องการ

<p align="right">(<a href="#readme-top">back to top</a>)</p>
