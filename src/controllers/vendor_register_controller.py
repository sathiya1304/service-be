from flask import Blueprint, request, jsonify
from src import db
from src.models.vendor_register_model import VendorRegister
import logging

def add_vendor_register():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        # Check if a record with the same email or mobile number already exists
        existing_vendor = VendorRegister.query.filter(
            (VendorRegister.email == data.get('email')) |
            (VendorRegister.mobile_number == data.get('mobile_number'))
        ).first()

        if existing_vendor:
            logging.warning("Vendor with the same email or mobile number already exists.")
            return jsonify({"message": "A vendor with this email or mobile number already exists.", "success": False}), 409

        # Create a new vendor record
        new_vendor = VendorRegister(
            business_name=data.get('business_name'),
            owner_name=data.get('owner_name'),
            email=data.get('email'),
            password=data.get('password'),  # Ensure this is hashed for security
            business_type=data.get('business_type'),
            mobile_number=data.get('mobile_number'),
            status="Active",
        )
        logging.debug(f"New vendor record: {new_vendor}")

        db.session.add(new_vendor)
        db.session.commit()

        return jsonify({"message": "Vendor registered successfully", "success": True}), 201

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Error registering vendor", "success": False, "msg": str(e)}), 500
