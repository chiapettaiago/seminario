from flask import render_template, redirect, url_for, session, request, flash
from routes.auth import login_required, get_user_data, update_user_progress, load_users, save_users
import hashlib
from datetime import datetime

def main():
    # Redireciona para o primeiro slide
    return redirect(url_for('slide', slide_number=1))

def slide(slide_number):
    """Renderiza um slide específico"""
    # Validar número do slide
    if slide_number < 1 or slide_number > 10:
        return redirect(url_for('slide', slide_number=1))
    
    # Calcular slides anterior e próximo
    prev_slide = slide_number - 1 if slide_number > 1 else None
    next_slide = slide_number + 1 if slide_number < 10 else None
    
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
    
    lessons_list = [
        {'number': 1, 'title': 'Bem-vindos ao Curso de Inglês', 'description': 'Introdução ao curso', 'completed': 1 <= completed_slides},
        {'number': 2, 'title': 'Objetivos de Aprendizado', 'description': 'Metas e expectativas', 'completed': 2 <= completed_slides},
        {'number': 3, 'title': 'Vocabulário Básico', 'description': 'Palavras essenciais do dia a dia', 'completed': 3 <= completed_slides},
        {'number': 4, 'title': 'Gramática: Presente Simples', 'description': 'Estruturas básicas do presente', 'completed': 4 <= completed_slides},
        {'number': 5, 'title': 'Quiz Interativo', 'description': 'Teste seus conhecimentos', 'completed': 5 <= completed_slides},
        {'number': 6, 'title': 'Frases Essenciais', 'description': 'Expressões importantes', 'completed': 6 <= completed_slides},
        {'number': 7, 'title': 'Números e Cores', 'description': 'Vocabulário numérico e cromático', 'completed': 7 <= completed_slides},
        {'number': 8, 'title': 'Exercício Interativo', 'description': 'Prática com drag and drop', 'completed': 8 <= completed_slides},
        {'number': 9, 'title': 'Prática de Conversação', 'description': 'Diálogos e pronunciação', 'completed': 9 <= completed_slides},
        {'number': 10, 'title': 'Parabéns!', 'description': 'Conclusão do curso', 'completed': 10 <= completed_slides}
    ]
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
        
        users = load_users()
        
        # Hash da senha para comparação
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if username in users and users[username]['password'] == password_hash:
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
        
        users = load_users()
        
        if username in users:
            flash('Nome de usuário já existe.', 'error')
            return render_template('register.html')
        
        # Criar novo usuário
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users[username] = {
            'password': password_hash,
            'email': email,
            'created_at': str(datetime.now())
        }
        
        save_users(users)
        
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