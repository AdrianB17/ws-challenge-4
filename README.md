# Challege4-ws

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
