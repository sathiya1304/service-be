from flask import Flask, jsonify
from src import create_app 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = create_app()
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  
jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(debug=True)
