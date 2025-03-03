import os
from flask import Blueprint, send_from_directory, render_template

static_bp = Blueprint('static_bp', __name__)

@static_bp.route('/', methods=['GET'])
def index():
    """Serve the index.html file"""
    return render_template('index.html')
