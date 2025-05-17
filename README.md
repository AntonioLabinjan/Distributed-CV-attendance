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
- povezat to na face recognition (onda se nodes moru stavit na svaki ulaz u zgradu i slat na centralni server koji sve bilježi)
- note to self: na renderu se vrti centralni server, nodes (kamere) delaju lokalno
