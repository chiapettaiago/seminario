from flask import render_template, redirect, url_for

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
    
    # Renderizar o template do slide específico
    template_name = f'slides/slide{slide_number}.html'
    
    return render_template(template_name, 
                         current_slide=slide_number,
                         prev_slide=prev_slide,
                         next_slide=next_slide)