import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.vendor_register_controller import add_vendor_register
vendor_register_bp = Blueprint('vendor_register', __name__, url_prefix='/vendor_register')




#vendorLogin
@vendor_register_bp.route('/', methods=['POST'])
def add_vendor_register_controller():
    return add_vendor_register()