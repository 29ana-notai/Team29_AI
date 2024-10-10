from flask import Flask
from celery import Celery
from app.config.logging_config import configure_logging

configure_logging()

celery = Celery(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.app_config.Config')
    
    celery.config_from_object('app.config.celery_config')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask

    from app import routes
    app.register_blueprint(routes.api)
    
    return app

app = create_app()