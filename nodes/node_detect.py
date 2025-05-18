# node/node_detect.py
import cv2
import torch
import requests
import time
from collections import deque

model = torch.hub.load('ultralytics/yolov5', 'yolov5n') 
model.classes = [0]  # samo osoba (COCO klasa 0)

NODE_ID = "Node-1"
SERVER_URL = "https://central-server-app-1.onrender.com/report"

cap = cv2.VideoCapture(0)

last_sent_time = 0
cooldown = 2  # sekunde između slanja detekcija

pending_queue = deque()  # fallback red za podatke koje nismo uspjeli poslati

def try_send(data):
    try:
        response = requests.post(SERVER_URL, json=data, timeout=3)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[Greška] Slanje neuspjelo: {e}")
        return False

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
        data = {"node_id": NODE_ID, "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}
        
        if try_send(data):
            last_sent_time = current_time
        else:
            pending_queue.append(data)

        time.sleep(5)  # da ne spammamo server

    # Pokušaj poslati podatke iz pending_queue
    if pending_queue:
        print(f"Pokušavam poslati {len(pending_queue)} zaostalih zapisa...")
        for _ in range(len(pending_queue)):
            item = pending_queue.popleft()
            if not try_send(item):
                pending_queue.append(item)
                break  # ako padne prvi, vjerojatno neće ni ostali - pričekaj sljedeći krug

    time.sleep(0.5)
