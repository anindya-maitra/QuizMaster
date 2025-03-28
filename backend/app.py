from flask import Flask
from app import createApp
from flask_cors import CORS

app = createApp()
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)