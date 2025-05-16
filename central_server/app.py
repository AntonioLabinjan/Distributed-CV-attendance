# central_server/app.py
from flask import Flask, request, jsonify, render_template_string, redirect
from datetime import datetime
import os
import queue
import threading
import atexit

app = Flask(__name__)
LOG_FILE = "detections.log"

# Queue za asinkrono logiranje
log_queue = queue.Queue()

# Worker thread koji piše u log
def log_worker():
    while True:
        log_line = log_queue.get()
        if log_line is None:  # Signal za kraj
            break
        with open(LOG_FILE, "a") as f:
            f.write(log_line)
            f.flush()  # odmah isprazni buffer (brže logiranje)
        log_queue.task_done()


# Pokretanje radničkog threada
worker_thread = threading.Thread(target=log_worker, daemon=True)
worker_thread.start()

# Čišćenje na izlasku
@atexit.register
def shutdown():
    log_queue.put(None)  # signal za shutdown
    worker_thread.join()

@app.route('/', methods=['GET', 'POST'])
def reroute():
    if request.method == 'POST':
        return redirect("/report")
    else:
        return redirect("/logs")

@app.route('/report', methods=['POST'])
def report_detection():
    data = request.json
    node_id = data.get("node_id")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"{timestamp} - Detected PERSON from node: {node_id}\n"
    print(log_line.strip())

    # Umjesto direktnog pisanja u file, šalji u red
    log_queue.put(log_line)

    return jsonify({"status": "received"}), 200

@app.route('/logs', methods=['GET'])
def view_logs():
    if not os.path.exists(LOG_FILE):
        logs = "Log file not found."
    else:
        # Zadnjih 100 linija za brže čitanje
        from collections import deque
        with open(LOG_FILE, "r") as f:
            logs = "".join(deque(f, maxlen=100))

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Detection Logs</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
            pre { white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h2> Detection Logs (auto-refresh every 3s)</h2>
        <pre>{{ logs }}</pre>
    </body>
    </html>
    """
    return render_template_string(html_template, logs=logs)

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("")  # možeš dodati header ako želiš

    app.run(host="0.0.0.0", port=5000, threaded=True)  # omogućuje više zahtjeva paralelno
