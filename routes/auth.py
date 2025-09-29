from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
import json
import os
from urllib.parse import urlparse, parse_qs

import ssl

import certifi
import pymysql
from pymysql import MySQLError
from pymysql.err import IntegrityError

auth_bp = Blueprint('auth', __name__)

# Armazenamento de progresso permanece em arquivo JSON
PROGRESS_FILE = 'data/user_progress.json'

# Configuração de banco de dados para usuários
DB_CONNECTION_URI = os.environ.get(
    'DATABASE_URL',
    'mysql://root:YoegMgp8vVoNNpyHxx1SJvuByU4gKqan@x4rc9k.stackhero-network.com:4782/root?useSSL=true&requireSSL=true'
)


def _parse_db_uri(uri):
    """Converte a URI de conexão em um dicionário aceito pelo PyMySQL."""
    parsed = urlparse(uri)
    if parsed.scheme != 'mysql':
        raise RuntimeError('DATABASE_URL deve usar o esquema mysql://')

    if not parsed.path or parsed.path == '/':
        raise RuntimeError('DATABASE_URL precisa incluir o nome do banco na rota')

    query = {key: values[0] for key, values in parse_qs(parsed.query).items()}

    config = {
        'host': parsed.hostname,
        'port': parsed.port or 3306,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/'),
        'autocommit': True,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    # Ativa TLS quando requerido pela conexão
    if query.get('requireSSL', 'false').lower() == 'true' or query.get('useSSL', 'false').lower() == 'true':
        config['ssl'] = {
            'ca': certifi.where(),
            'cert_reqs': ssl.CERT_REQUIRED,
        }

    return config


def get_db_connection():
    """Cria uma nova conexão com o banco de dados MySQL."""
    config = _parse_db_uri(DB_CONNECTION_URI)
    try:
        connection = pymysql.connect(**config)
        return connection
    except MySQLError as exc:
        raise RuntimeError('Não foi possível conectar ao banco de dados.') from exc


def ensure_users_table(connection=None):
    """Garante que a tabela de usuários exista no banco de dados."""
    conn = connection or get_db_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        conn.commit()
    except MySQLError as exc:
        raise RuntimeError('Não foi possível preparar a tabela de usuários.') from exc
    finally:
        if cursor:
            cursor.close()
        if connection is None:
            conn.close()


def get_user_by_username(username):
    """Busca um usuário pelo nome de usuário."""
    conn = get_db_connection()
    cursor = None
    try:
        ensure_users_table(conn)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, password, email, created_at FROM users WHERE username = %s",
            (username,)
        )
        return cursor.fetchone()
    except MySQLError as exc:
        raise RuntimeError('Erro ao consultar usuário no banco de dados.') from exc
    finally:
        if cursor:
            cursor.close()
        conn.close()


def create_user(username, password_hash, email):
    """Cria um novo usuário no banco de dados."""
    conn = get_db_connection()
    cursor = None
    try:
        ensure_users_table(conn)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, password_hash, email)
        )
        conn.commit()
    except IntegrityError as exc:
        raise RuntimeError('Nome de usuário já está em uso.') from exc
    except MySQLError as exc:
        raise RuntimeError('Erro ao salvar o usuário no banco de dados.') from exc
    finally:
        if cursor:
            cursor.close()
        conn.close()

def ensure_data_dir():
    """Garante que o diretório de dados exista."""
    if not os.path.exists('data'):
        os.makedirs('data')


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
        'courses_completed': 1 if len(user_progress['completed_slides']) >= 8 else 0,
        'total_study_time': f"{user_progress['time_spent']} minutos",
        'streak_days': user_progress['study_streak'],
        'favorite_topics': ['Vocabulário', 'Gramática', 'Conversação'],
        'next_goal': 'Completar curso intermediário',
        'progress': {
            'completed_slides': len(user_progress['completed_slides']),
            'total_slides': 8,
            'completion_percentage': int((len(user_progress['completed_slides']) / 8) * 100),
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
    if len(user_progress['completed_slides']) >= 8:
        achievements.add('Curso Finalizado')
    
    user_progress['achievements'] = list(achievements)
    
    save_user_progress(progress_data)
