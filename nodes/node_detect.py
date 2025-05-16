# node/node_detect.py
import cv2
import torch
import requests
import time

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # najmanji model
model.classes = [0]  # samo osoba (COCO klasa 0)

NODE_ID = "Node-1"
SERVER_URL = "http://127.0.0.1:5000/report"

cap = cv2.VideoCapture(0)

last_sent_time = 0
cooldown = 2  # sekunde između slanja detekcija

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)
    detections = results.pred[0]
    person_detected = any(d[5] == 0 for d in detections)

    current_time = time.time()
    if person_detected and (current_time - last_sent_time) > cooldown:
        print(" Osoba detektirana! Slanje na server...")
        try:
            requests.post(SERVER_URL, json={"node_id": NODE_ID}, timeout=2)
            last_sent_time = current_time
        except Exception as e:
            print(f"[Greška] Nije moguće poslati serveru: {e}")

        
        time.sleep(5)  # spriječi spamanje servera

    time.sleep(0.5)  # obrada svakih pola sekunde
