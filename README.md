# Blind-Assist
FPGA Navigation System for the Visually Impaired is a hybrid hardware and software project that combines real time computer vision with FPGA based decision logic to assist visually impaired individuals in safe navigation.
# 🤖 FPGA Navigation System for the Visually Impaired

## 📌 Overview
This project presents a hybrid AI + FPGA-based navigation system designed to assist visually impaired individuals. It combines real-time object detection with hardware-based decision-making for ultra-fast and reliable navigation assistance.

## ⚙️ Features
- Real-time object detection using YOLOv8  
- Zone-based obstacle classification (Left, Center, Right)  
- FPGA-based priority decision logic (Center > Left > Right)  
- Low-latency hardware response  
- Voice alert feedback system  

## 🧠 Tech Stack
- Python  
- YOLOv8  
- OpenCV  
- Verilog HDL  
- Icarus Verilog  
- GTKWave  
- pyttsx3  

## 🔄 Workflow
1. Capture video using camera  
2. Detect objects using YOLOv8  
3. Segment frame into zones using OpenCV  
4. Convert detections into digital signals  
5. Process signals using FPGA (Verilog logic)  
6. Generate voice alerts  

