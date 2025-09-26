from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import json
import os

auth_bp = Blueprint('auth', __name__)

# Arquivo para armazenar usuários (em produção, usar banco de dados)
USERS_FILE = 'data/users.json'
PROGRESS_FILE = 'data/user_progress.json'

def ensure_data_dir():
    """Garante que o diretório data existe"""
    if not os.path.exists('data'):
        os.makedirs('data')

def load_users():
    """Carrega usuários do arquivo JSON"""
    ensure_data_dir()
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Salva usuários no arquivo JSON"""
    ensure_data_dir()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_user_progress():
    """Carrega progresso dos usuários"""
    ensure_data_dir()
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_progress(progress_data):
    """Salva progresso dos usuários"""
    ensure_data_dir()
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress_data, f, indent=2)

def login_required(f):
    """Decorator para páginas que exigem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_data(username):
    """Obtém dados completos do usuário incluindo progresso"""
    progress_data = load_user_progress()
    user_progress = progress_data.get(username, {
        'completed_slides': [],
        'quiz_scores': {},
        'time_spent': 0,
        'vocabulary_learned': 0,
        'achievements': [],
        'last_slide': 1,
        'study_streak': 1
    })
    
    return {
        'name': username.title(),
        'level': 'Iniciante' if len(user_progress['completed_slides']) < 5 else 'Intermediário',
        'courses_completed': 1 if len(user_progress['completed_slides']) >= 10 else 0,
        'total_study_time': f"{user_progress['time_spent']} minutos",
        'streak_days': user_progress['study_streak'],
        'favorite_topics': ['Vocabulário', 'Gramática', 'Conversação'],
        'next_goal': 'Completar curso intermediário',
        'progress': {
            'completed_slides': len(user_progress['completed_slides']),
            'total_slides': 10,
            'completion_percentage': int((len(user_progress['completed_slides']) / 10) * 100),
            'time_spent': f"{user_progress['time_spent']} minutos",
            'quiz_score': f"{sum(user_progress['quiz_scores'].values())}/{len(user_progress['quiz_scores']) * 10}" if user_progress['quiz_scores'] else "0/0",
            'vocabulary_learned': user_progress['vocabulary_learned'],
            'achievements': user_progress['achievements']
        }
    }

def update_user_progress(username, slide_number):
    """Atualiza progresso do usuário ao completar um slide"""
    progress_data = load_user_progress()
    
    if username not in progress_data:
        progress_data[username] = {
            'completed_slides': [],
            'quiz_scores': {},
            'time_spent': 0,
            'vocabulary_learned': 0,
            'achievements': [],
            'last_slide': 1,
            'study_streak': 1
        }
    
    user_progress = progress_data[username]
    
    # Adicionar slide aos completados se não estiver já
    if slide_number not in user_progress['completed_slides']:
        user_progress['completed_slides'].append(slide_number)
        user_progress['time_spent'] += 5  # 5 minutos por slide
        
        # Adicionar vocabulário baseado no slide
        vocab_by_slide = {3: 10, 6: 8, 7: 12}  # Slides com vocabulário
        if slide_number in vocab_by_slide:
            user_progress['vocabulary_learned'] += vocab_by_slide[slide_number]
    
    # Atualizar último slide
    user_progress['last_slide'] = max(user_progress['last_slide'], slide_number)
    
    # Adicionar conquistas
    achievements = set(user_progress['achievements'])
    if slide_number == 1:
        achievements.add('Primeiro Slide Completado')
    if slide_number == 5:
        achievements.add('Quiz Master')
    if slide_number >= 3:
        achievements.add('Vocabulário Básico')
    if slide_number >= 9:
        achievements.add('Conversação Iniciante')
    if len(user_progress['completed_slides']) >= 10:
        achievements.add('Curso Finalizado')
    
    user_progress['achievements'] = list(achievements)
    
    save_user_progress(progress_data)