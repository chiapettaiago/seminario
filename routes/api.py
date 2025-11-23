from flask import Blueprint, jsonify, request, session, current_app
from functools import wraps
import hashlib
import os
import re
from routes.auth import (
    get_user_data,
    update_user_progress,
    get_user_by_username,
    create_user,
    get_db_connection
)
from routes.main import LESSONS_DATA

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 503

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/me', methods=['GET'])
@api_login_required
def get_me():
    user_data = get_user_data(session['user'])
    return jsonify(user_data)

@api_bp.route('/lessons', methods=['GET'])
def get_lessons():
    completed_slides = 0
    if 'user' in session:
        user_data = get_user_data(session['user'])
        completed_slides = user_data['progress']['completed_slides']
    
    lessons_list = []
    for lesson in LESSONS_DATA:
        lesson_copy = lesson.copy()
        lesson_copy['completed'] = lesson['number'] <= completed_slides
        lessons_list.append(lesson_copy)
        
    return jsonify({'lessons': lessons_list})

@api_bp.route('/lessons/<int:lesson_number>/content', methods=['GET'])
def get_lesson_content(lesson_number):
    if lesson_number < 1 or lesson_number > 8:
        return jsonify({'error': 'Invalid lesson number'}), 404
        
    template_path = os.path.join(current_app.root_path, 'templates', 'slides', f'slide{lesson_number}.html')
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract content block using regex
        # Matches {% block content %} ... {% endblock %}
        # Using non-greedy match for content
        match = re.search(r'{%\s*block\s+content\s*%}(.*?){%\s*endblock\s*%}', content, re.DOTALL)
        
        if match:
            html_content = match.group(1).strip()
            return jsonify({'content': html_content})
        else:
            # Fallback: return the whole file if block not found (unlikely)
            return jsonify({'error': 'Content block not found in template'}), 500
            
    except FileNotFoundError:
        return jsonify({'error': 'Lesson content file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    if not data or 'slide_number' not in data:
        return jsonify({'error': 'Missing slide_number'}), 400
    
    slide_number = data['slide_number']
    if not isinstance(slide_number, int) or slide_number < 1 or slide_number > 8:
        return jsonify({'error': 'Invalid slide_number'}), 400
        
    if 'user' in session:
        update_user_progress(session['user'], slide_number)
        return jsonify({'success': True, 'message': f'Progress updated to slide {slide_number}'})
    
    return jsonify({'success': True, 'message': f'Slide {slide_number} recorded (guest mode)'})

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
        
    username = data['username'].lower().strip()
    password = data['password']
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        user_record = get_user_by_username(username)
    except RuntimeError:
        return jsonify({'error': 'Database error'}), 500

    if user_record and user_record['password'] == password_hash:
        session['user'] = username
        return jsonify({'success': True, 'message': 'Logged in successfully', 'user': username})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    username = data.get('username', '').lower().strip()
    password = data.get('password', '')
    email = data.get('email', '')
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
    try:
        existing_user = get_user_by_username(username)
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409
            
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        create_user(username, password_hash, email)
        
        session['user'] = username
        return jsonify({'success': True, 'message': 'User created successfully', 'user': username}), 201
        
    except RuntimeError as exc:
        error_msg = str(exc)
        if 'já está em uso' in error_msg:
            return jsonify({'error': error_msg}), 409
        return jsonify({'error': error_msg}), 500

@api_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})
