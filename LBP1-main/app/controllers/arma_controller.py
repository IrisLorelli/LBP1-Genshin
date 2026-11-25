from flask import Blueprint, request, redirect, url_for, session, flash, current_app
from app.models.arma_model import Arma
from app.utils.auth_middleware import login_required

arma_bp = Blueprint('armas', __name__, url_prefix='/armas')

TIPOS_VALIDOS = {'Arco', 'Espada', 'Espadão', 'Lança', 'Catalisador'}

@arma_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar():
    user_id = session['user_id']
    nome = request.form.get('nome', '').strip()
    tipo = request.form.get('tipo', '').strip()
    raridade_raw = request.form.get('raridade', '').strip()
    nivel_raw = request.form.get('nivel', '').strip()

    # Validação back-end
    if not nome or not tipo or not raridade_raw or not nivel_raw:
        flash('Todos os campos da arma são obrigatórios!', 'danger')
        return redirect(url_for('main.dashboard'))

    if len(nome) < 2 or len(nome) > 60:
        flash('O nome da arma deve ter entre 2 e 60 caracteres.', 'danger')
        return redirect(url_for('main.dashboard'))

    if tipo not in TIPOS_VALIDOS:
        flash('Tipo de arma inválido.', 'danger')
        return redirect(url_for('main.dashboard'))

    try:
        raridade = int(raridade_raw)
        nivel = int(nivel_raw)
        if raridade not in (3, 4, 5) or not (1 <= nivel <= 90):
            raise ValueError
    except ValueError:
        flash('Raridade (3 a 5) ou nível (1 a 90) da arma inválidos.', 'danger')
        return redirect(url_for('main.dashboard'))

    nova_arma = Arma(
        usuario_id=user_id,
        nome=nome,
        tipo=tipo,
        raridade=raridade,
        nivel=nivel
    )
    nova_arma.salvar()

    current_app.logger.info(f'Usuário {user_id} cadastrou a arma: {nome}')
    flash(f'Arma "{nome}" adicionada ao inventário!', 'success')
    return redirect(url_for('main.dashboard'))

@arma_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    user_id = session['user_id']
    excluida = Arma.excluir(id, user_id)

    if excluida:
        current_app.logger.info(f'Usuário {user_id} excluiu a arma ID {id}')
        flash('Arma removida do inventário.', 'success')
    else:
        current_app.logger.warning(f'Tentativa inválida de exclusão da arma ID {id} pelo usuário {user_id}')
        flash('Arma não encontrada ou você não tem permissão para excluí-la.', 'danger')

    return redirect(url_for('main.dashboard'))