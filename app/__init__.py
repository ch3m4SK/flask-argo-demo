from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from prometheus_client import Counter, Gauge, start_http_server
import time  # Importación añadida para time.time()

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Métricas Prometheus
    REQUEST_COUNT = Counter('flask_request_count', 'Total HTTP Requests')  # Corregido typo (EQUEST_COUNT -> REQUEST_COUNT)
    LATENCY = Gauge('flask_request_latency_seconds', 'Request latency')
    ERROR_COUNT = Counter('flask_error_count', 'Total HTTP Errors', ['status_code'])  # Métrica adicional recomendada

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        latency = time.time() - request.start_time
        LATENCY.set(latency)
        REQUEST_COUNT.inc()
        
        # Registrar errores HTTP (4xx, 5xx)
        if 400 <= response.status_code < 600:
            ERROR_COUNT.labels(status_code=response.status_code).inc()
            
        return response

    # Inicia servidor de métricas en puerto 8000 (solo en producción)
    start_http_server(8000)
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    
    # Registrar rutas
    from app.routes import register_routes
    register_routes(app)
    
    with app.app_context():
        db.create_all()
    
    return app