Distributed upgrade idea for CV attendance module

DONE: 
- čekat da fini docker build
- pushat na dockerhub
  Prve dvi stavke OK: https://hub.docker.com/repository/docker/antoniolabinjan/central_server_app/general
- iz dockerhuba na render
- "https://central-server-app-1.onrender.com/report"
- render link stavit u node_detect.py (pod SERVER_URL)

TODO...provjerit na više kompjuteri istovremeno 
- obavezno stavit drugo ime u svaki node jer će škopjat ako ne
