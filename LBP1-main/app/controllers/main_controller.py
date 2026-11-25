from flask import Blueprint, render_template, session, request, make_response, redirect, url_for
from app.models.personagem_model import Personagem
from app.models.arma_model import Arma
from app.utils.auth_middleware import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    tema = request.cookies.get('tema', 'escuro')

    personagens = Personagem.listar_por_usuario(user_id)
    armas = Arma.listar_por_usuario(user_id)

    return render_template(
        'main/dashboard.html',
        personagens=personagens,
        armas=armas,
        tema=tema
    )

@main_bp.route('/alternar-tema', methods=['POST'])
@login_required
def alternar_tema():
    tema_atual = request.cookies.get('tema', 'escuro')
    novo_tema = 'claro' if tema_atual == 'escuro' else 'escuro'

    resposta = make_response(redirect(url_for('main.dashboard')))
    resposta.set_cookie('tema', novo_tema, max_age=60 * 60 * 24 * 30)
    return resposta