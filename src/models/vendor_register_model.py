from src import db

class VendorRegister(db.Model):
    __tablename__ = 'vendor_register'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed password
    business_type = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.String(20), default="Active")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
