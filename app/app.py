from bottle import Bottle, request, response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Bottle()

# Create a Prometheus counter
heavywork_counter = Counter('heavywork_requests_total', 'Total number of heavywork requests')

@app.get('/')
def index():
    return {"message": "Server is running"}

@app.post('/heavywork')
def heavywork():
    heavywork_counter.inc()
    response.status = 202
    return {"message": "Heavy work started"}


@app.post('/lightwork')
def lightwork():
    return {"message": "Light work done"}

@app.get('/metrics')
def metrics():
    response.content_type = CONTENT_TYPE_LATEST
    return generate_latest()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)