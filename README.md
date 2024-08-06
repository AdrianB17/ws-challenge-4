# Challege4-WS

Nos enfocamos en la flexibilidad y automatización del escalamiento para aplicaciones desplegadas sobre Kubernetes, el cual a su vez reside sobre una arquitectura de nube privada provista por Whitestack. En específico, se pretende utilizar métricas generadas por una app, prometheus y el HPA de kubernetes.

<img width="712" alt="image" src="https://github.com/user-attachments/assets/442bc6eb-1ed8-43e9-a3e1-874b74c2d5ac">

# Adaptar la aplicación web

Usamos la libreria python "prometheus_client" para obtener las metricas. Agregamos un contador de requests solo para la ruta /heavywork, expuestos en
/metrics en formato prometheus.

__app.py__

```python
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST  #Agregamos el modulo

# Create a Prometheus counter
heavywork_counter = Counter('heavywork_requests_total', 'Total number of heavywork requests')    #Agregamos el contador para la ruta /heavyworks

@app.get('/metrics') 
def metrics():
    response.content_type = CONTENT_TYPE_LATEST
    return generate_latest()
```

# Desplegar la aplicación
__Crear la imagen y subir a Docker Hub__

Crear la imagen con el dockerfile y subirlo a un repositorio publico
```shell
$ docker build -t adrianb17/challenge4-py:latest .
$ docker push adrianb17/challenge4-py:latest
```

__Crear un Chart Helm y desplegarlo al cluster__

Creamos un chart helm y modificamos el values.yaml, asi como los templates. Luego, desplegamos el chart a K8S
```shell
$ helm create prometheus
$ helm install prometheus prometheus
```
IMPORTANTE: En este caso, ya tenemos  el chart helm. Entonces, solo desplegamos el chart con el comando "helm install"

__Validar disponibilidad de la aplicacion web__
Desplegamos la aplicacion con el chart helm creado, utilizando el comando "helm install prometheus prometheus"
```shell
$ helm install prometheus prometheus
0805 23:00:10.163860    4588 warnings.go:70] Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens.
W0805 23:00:10.286424    4588 warnings.go:70] Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens.
NAME: prometheus
LAST DEPLOYED: Mon Aug  5 23:00:06 2024
NAMESPACE: challenger-007
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  http://myapp.201.217.240.66.nip.io/
```
Al ingresar la ip que se muestra en el output y con el puerto 8080, podemos visualizar lo siguiente:
<img width="616" alt="image" src="https://github.com/user-attachments/assets/10d3b7b1-f783-4c7f-b4bf-1065611d91c9">

OBSERVACION: En la aplicacion le agregue la ruta por defecto, para que nos muestra si el pod esta en el estado "running", asi como el service y el ingress estan configurados correctamente.

# Desplegar la aplicación
Agregamos el archivo servicemonitor.yaml en el directorio templates
```yaml
# Crear serviceMonitor para obtención de métricas
Agregamos el archivo servicemonitor.yaml en el directorio 'templates'
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "prometheus.name" . }}
  namespace: {{ .Release.Namespace }}
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: {{ include "prometheus.name" . }}
  endpoints:
    - port: "8080"
      path: /metrics
      interval: 15s
```
IMPORTANTE: En este caso, ya esta desplegado con el primer comando 'helm install'. Si queremos modificar el chart helm, para actualizar el despliegue utilizamos el comando 'helm upgrade prometheus prometheus'

Y visualizamos que en la ruta /metrics, ya podemos visualizar las metricas
<img width="793" alt="image" src="https://github.com/user-attachments/assets/e10a6492-f95b-48c5-8a13-2daac230076e">

# Instalar y configurar Prometheus Adapter
Instalamos Prometheus Adapter

```shell
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
$ helm install prometheus prometheus-community/prometheus
```

# Crear HPA usando la métrica externa
Para visualizar si las metricas estan siendo detectadas por prometheus, ejecuatamos el siguiente comando y buscamos la metrica
```shell
$ kubectl port-forward svc/prometheus-operated -n monitoring 9093:9090
```
<img width="1426" alt="image" src="https://github.com/user-attachments/assets/54983203-7cae-41c9-b1c7-b2e99c8e0881">

OBSERVACION: Si bien las metricas se muestran en la ruta /metrics, prometheus no esta recibiendo las metricas del pod del namespace asignado :(

# Generar carga y analizar
Modificamos el script para generar trafico en la ruta /heavywork
__app.py__

```python
host, port, path = ('myapp.201.217.240.66.nip.io', 8080, '/heavywork')
```

```shell
$ python3 generate_load.py 
202 {"message": "Heavy work started"}
202 {"message": "Heavy work started"}
202 {"message": "Heavy work started"}
202 {"message": "Heavy work started"}
```
Y visualizamos que la metrica se actualiza:
<img width="809" alt="image" src="https://github.com/user-attachments/assets/fc7d06d8-fb11-40c1-b807-40f7c69d9a02">


