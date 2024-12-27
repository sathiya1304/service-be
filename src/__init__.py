from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('src.config.Config')
    # Alternatively, use a configuration file
    # app.config.from_pyfile('config.py')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    #src
    from src.routes.vendor_login import vendor_login_bp
    from src.routes.vendor_register_routes import vendor_register_bp
    from src.routes.category import category_bp
    from src.routes.products import product_bp

    
     # Register blueprints
    app.register_blueprint(vendor_login_bp)
    app.register_blueprint(vendor_register_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)

    return app
