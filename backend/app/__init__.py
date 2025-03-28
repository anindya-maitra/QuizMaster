from flask import Flask
from .route import main
def createApp():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app