from flask import Flask
from flask_cors import CORS
from app import api

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)


api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8040)

