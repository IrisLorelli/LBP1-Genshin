from functools import wraps
from flask import session, redirect, url_for, flash, g
from app.models.user_model import Usuario

def login_required(f):
    """Garante que a rota só seja acessada por um usuário autenticado e existente no banco."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))

        usuario = Usuario.buscar_por_id(user_id)
        if not usuario:
            session.clear()
            flash('Sessão inválida ou usuário não encontrado. Faça login novamente.', 'danger')
            return redirect(url_for('auth.login'))

        g.usuario = usuario
        return f(*args, **kwargs)
    return decorated_function