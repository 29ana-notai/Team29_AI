from flask import Flask
from celery import Celery
from app.celery_config import broker_url, result_backend, task_serializer, result_serializer, accept_content, timezone, enable_utc
from app.logging_config import configure_logging

configure_logging()

celery = Celery(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    celery.conf.update(
        broker=broker_url,
        backend=result_backend,
        task_serializer=task_serializer,
        result_serializer=result_serializer,
        accept_content=accept_content,
        timezone=timezone,
        enable_utc=enable_utc
    )
    celery.config_from_object('app.celery_config')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask

    from app import routes
    app.register_blueprint(routes.api)
    
    return app

app = create_app()