from flask import Blueprint, request, jsonify, render_template, current_app
import os
from werkzeug.utils import secure_filename
import logging
from .model import predict_image

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@main_bp.route('/predict', methods=['POST'])
def predict():
    """Predict tumor type from uploaded image"""
    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400
        
        # Save file
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        
        logger.info(f"Processing image: {filename}")
        
        # Get prediction
        result = predict_image(image_path)
        
        # Clean up uploaded file
        try:
            os.remove(image_path)
        except:
            pass
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Internal server error during prediction'}), 500