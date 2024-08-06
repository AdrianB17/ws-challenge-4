# Challege4-WS

Nos enfocamos en la flexibilidad y automatización del escalamiento para aplicaciones desplegadas sobre Kubernetes, el cual a su vez reside sobre una arquitectura de nube privada provista por Whitestack. En específico, se pretende utilizar métricas generadas por una app, prometheus y el HPA de kubernetes.

<img width="712" alt="image" src="https://github.com/user-attachments/assets/442bc6eb-1ed8-43e9-a3e1-874b74c2d5ac">

# Adaptar la aplicación web

Usamos la libreria python "prometheus_client" para obtener las metricas. Agregamos un contador de requests solo para la ruta /heavywork, expuestos en
/metrics en formato prometheus.

__app.py__

Un módulo de Terraform se organiza en un conjunto de archivos y directorios que juntos definen una parte específica de la infraestructura.

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

OBSERVACION: En la aplicacion le agregue la ruta por defecto, para que nos muestra si el servidor esta en el estado "running"


