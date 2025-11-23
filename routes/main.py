from flask import render_template, redirect, url_for, session, request, flash
from routes.auth import (
    login_required,
    get_user_data,
    update_user_progress,
    get_user_by_username,
    create_user,
)
import hashlib

LESSONS_DATA = [
    {'number': 1, 'title': 'Bem-vindos ao Seminário de Inglês', 'description': 'Introdução ao seminário'},
    {'number': 2, 'title': 'Como o Sistema Funciona', 'description': 'Explicação do sistema de ensino'},
    {'number': 3, 'title': 'Vocabulário Básico & Sistema de Áudio', 'description': 'Palavras essenciais com pronúncia'},
    {'number': 4, 'title': 'Gramática: Present Perfect', 'description': 'Estruturas do Present Perfect'},
    {'number': 5, 'title': 'Exercício Interativo: Simple Past', 'description': 'Prática com drag and drop'},
    {'number': 6, 'title': 'Advérbios em Inglês', 'description': 'Advérbios importantes'},
    {'number': 7, 'title': 'Present Perfect em Ação', 'description': 'Present Perfect na prática'},
    {'number': 8, 'title': 'Prática de Conversação', 'description': 'Diálogo guiado e exercícios'},
    {'number': 9, 'title': 'Expressões Idiomáticas', 'description': 'Frases e expressões comuns'},
    {'number': 10, 'title': 'Revisão Geral', 'description': 'Consolidação de conteúdo'},
    {'number': 11, 'title': 'Passive Voice - Voz Passiva', 'description': 'Gramática avançada: voz passiva'},
    {'number': 12, 'title': 'Conditional Sentences', 'description': 'Sentenças condicionais em inglês'},
    {'number': 13, 'title': 'Conclusão e Parabéns!', 'description': 'Parabéns - Curso finalizado!'}
]

def main():
    # Redireciona para o primeiro slide
    return redirect(url_for('slide', slide_number=1))

def slide(slide_number):
    """Renderiza um slide específico"""
    # Validar número do slide
    if slide_number < 1 or slide_number > 13:
        return redirect(url_for('slide', slide_number=1))
    
    # Calcular slides anterior e próximo
    prev_slide = slide_number - 1 if slide_number > 1 else None
    next_slide = slide_number + 1 if slide_number < 13 else None
    
    # Se o usuário estiver logado, atualizar progresso
    if 'user' in session:
        update_user_progress(session['user'], slide_number)
    
    # Renderizar o template do slide específico
    template_name = f'slides/slide{slide_number}.html'
    
    return render_template(template_name, 
                         current_slide=slide_number,
                         prev_slide=prev_slide,
                         next_slide=next_slide)

@login_required
def lessons():
    """Página com lista de todas as lições - REQUER LOGIN"""
    user_data = get_user_data(session['user'])
    completed_slides = user_data['progress']['completed_slides']
    
    lessons_list = []
    for lesson in LESSONS_DATA:
        lesson_copy = lesson.copy()
        lesson_copy['completed'] = lesson['number'] <= completed_slides
        lessons_list.append(lesson_copy)

    return render_template('lessons.html', lessons=lessons_list, user=user_data)

@login_required
def progress():
    """Página de progresso do usuário - REQUER LOGIN"""
    user_data = get_user_data(session['user'])
    return render_template('progress.html', progress=user_data['progress'], user=user_data)

@login_required
def profile():
    """Página de perfil do usuário - REQUER LOGIN"""
    user_data = get_user_data(session['user'])
    return render_template('profile.html', user=user_data)

def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username'].lower().strip()
        password = request.form['password']
        
        # Hash da senha para comparação
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            user_record = get_user_by_username(username)
        except RuntimeError:
            flash('Não foi possível acessar o banco de dados. Tente novamente mais tarde.', 'error')
            return render_template('login.html')

        if user_record and user_record['password'] == password_hash:
            session['user'] = username
            flash(f'Bem-vindo(a), {username.title()}!', 'success')
            
            # Redirecionar para a página solicitada ou dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('lessons'))
        else:
            flash('Usuário ou senha incorretos.', 'error')
    
    return render_template('login.html')

def register():
    """Página de registro"""
    if request.method == 'POST':
        username = request.form['username'].lower().strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        
        # Validações
        if len(username) < 3:
            flash('Nome de usuário deve ter pelo menos 3 caracteres.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Senhas não coincidem.', 'error')
            return render_template('register.html')
        
        try:
            existing_user = get_user_by_username(username)
        except RuntimeError:
            flash('Não foi possível acessar o banco de dados. Tente novamente mais tarde.', 'error')
            return render_template('register.html')

        if existing_user:
            flash('Nome de usuário já existe.', 'error')
            return render_template('register.html')

        # Criar novo usuário
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            create_user(username, password_hash, email)
        except RuntimeError as exc:
            flash(str(exc), 'error')
            return render_template('register.html')

        # Login automático
        session['user'] = username
        flash(f'Conta criada com sucesso! Bem-vindo(a), {username.title()}!', 'success')
        return redirect(url_for('lessons'))
    
    return render_template('register.html')

def logout():
    """Logout do usuário"""
    if 'user' in session:
        flash(f'Até logo, {session["user"].title()}!', 'info')
        session.pop('user', None)
    return redirect(url_for('slide', slide_number=1))
