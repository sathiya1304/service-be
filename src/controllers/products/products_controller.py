import time
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import json
import base64
from src import db
from src.models.products_model import ProductDetail  # Adjust according to your model path

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def fix_base64_padding(base64_string):
    """Fix missing padding in a base64 string if necessary."""
    try:
        # Calculate the missing padding length
        missing_padding = len(base64_string) % 4
        if missing_padding:
            base64_string += '=' * (4 - missing_padding)
        return base64_string
    except Exception as e:
        print(f"Error fixing base64 padding: {str(e)}")
        return base64_string  # Return the original string if there's an error

def add_product():
    """Add a new product from JSON data, including decoding base64-encoded images."""
    data = request.get_json()  # This should be JSON data
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Check for required fields
    required_fields = ['product_name', 'category_id', 'price', 'sku', 'stock_quantity', 'vendor_id', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    image_data = data.get('product_images', [])
    image_names = []
    for img_base64 in image_data:
        try:
            # Correct the base64 padding if necessary
            if ',' in img_base64:
                _, encoded = img_base64.split(',', 1)
            else:
                encoded = img_base64
            
            encoded = fix_base64_padding(encoded)  # Apply padding fix
            img_bytes = base64.b64decode(encoded)  # Decode the base64 string

            filename = secure_filename(f"image_{int(time.time())}.jpg")
            img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_bytes)
            image_names.append(filename)
        except Exception as e:
            return jsonify({"error": f"Failed to decode and save image: {str(e)}"}), 500

    try:
        new_product = ProductDetail(
            product_name=data['product_name'],
            description=data.get('description', ''),
            category_id=int(data['category_id']),
            price=float(data['price']),
            discount_price=float(data.get('discount_price', 0)),
            sku=data['sku'],
            stock_quantity=int(data['stock_quantity']),
            weight=float(data['weight']),
            dimensions=json.dumps(data.get('dimensions', {})),
            tags=json.dumps(data.get('tags', [])),
            product_images=json.dumps(image_names),
            vendor_id=int(data['vendor_id']),
            status=data['status']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully", "product_id": new_product.product_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add product: {str(e)}"}), 500


def edit_product(product_id):
    """Edit an existing product."""
    product = ProductDetail.query.get_or_404(product_id)
    data = request.form
    images = request.files.getlist('product_images')

    if images:
        # Delete old images if replacing
        old_images = json.loads(product.product_images)
        for image_name in old_images:
            try:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))
            except OSError:
                pass  # Handle error if file does not exist

        image_names = []
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                image_names.append(filename)
        product.product_images = json.dumps(image_names)

    product.product_name = data['product_name']
    product.description = data.get('description', product.description)
    product.category_id = data['category_id']
    product.price = float(data['price'])
    product.discount_price = float(data.get('discount_price', product.discount_price))
    product.sku = data['sku']
    product.stock_quantity = int(data['stock_quantity'])
    product.weight = float(data.get('weight', product.weight))
    product.dimensions = json.loads(data.get('dimensions', '{}'))
    product.tags = json.loads(data.get('tags', '[]'))
    product.vendor_id = int(data['vendor_id'])
    product.status = data.get('status', product.status)

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

def delete_product(product_id):
    """Mark a product as inactive instead of deleting it."""
    product = ProductDetail.query.get_or_404(product_id)
    product.status = "Inactive"
    db.session.commit()
    return jsonify({"message": "Product marked as inactive successfully"}), 200

def fetch_product():
    """Fetch all active products."""
    products = ProductDetail.query.filter_by(status='Active').all()
    product_list = [{
        "product_id": product.product_id,
        "product_name": product.product_name,
        "description": product.description,
        "category_id": product.category_id,
        "price": product.price,
        "discount_price": product.discount_price,
        "sku": product.sku,
        "stock_quantity": product.stock_quantity,
        "weight": product.weight,
        "dimensions": product.dimensions,
        "tags": product.tags,
        "product_images": json.loads(product.product_images),
        "vendor_id": product.vendor_id,
        "status": product.status
    } for product in products]

    return jsonify(product_list)
