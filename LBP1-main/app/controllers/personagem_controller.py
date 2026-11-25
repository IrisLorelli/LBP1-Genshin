from flask import Blueprint, request, redirect, url_for, session, flash, current_app
from app.models.personagem_model import Personagem
from app.utils.auth_middleware import login_required

personagem_bp = Blueprint('personagens', __name__, url_prefix='/personagens')

ELEMENTOS_VALIDOS = {'Pyro', 'Hydro', 'Anemo', 'Electro', 'Dendro', 'Cryo', 'Geo'}
ARMAS_VALIDAS = {'Arco', 'Espada', 'Espadão', 'Lança', 'Catalisador'}

@personagem_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar():
    user_id = session['user_id']
    nome = request.form.get('nome', '').strip()
    elemento = request.form.get('elemento', '').strip()
    arma = request.form.get('arma', '').strip()
    raridade_raw = request.form.get('raridade', '').strip()

    # Validação dados back-end
    if not nome or not elemento or not arma or not raridade_raw:
        flash('Todos os campos do personagem são obrigatórios!', 'danger')
        return redirect(url_for('main.dashboard'))

    if len(nome) < 2 or len(nome) > 50:
        flash('O nome do personagem deve ter entre 2 e 50 caracteres.', 'danger')
        return redirect(url_for('main.dashboard'))

    if elemento not in ELEMENTOS_VALIDOS or arma not in ARMAS_VALIDAS:
        flash('Elemento ou tipo de arma inválido.', 'danger')
        return redirect(url_for('main.dashboard'))

    try:
        raridade = int(raridade_raw)
        if raridade not in (4, 5):
            raise ValueError
    except ValueError:
        flash('A raridade do personagem deve ser 4 ou 5 estrelas.', 'danger')
        return redirect(url_for('main.dashboard'))

    novo = Personagem(
        usuario_id=user_id,
        nome=nome,
        elemento=elemento,
        arma=arma,
        raridade=raridade
    )
    novo.salvar()

    current_app.logger.info(f'Usuário {user_id} cadastrou o personagem: {nome}')
    flash(f'Personagem "{nome}" cadastrado com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))

@personagem_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    user_id = session['user_id']
    excluido = Personagem.excluir(id, user_id)

    if excluido:
        current_app.logger.info(f'Usuário {user_id} excluiu o personagem ID {id}')
        flash('Personagem removido da coleção.', 'success')
    else:
        current_app.logger.warning(f'Tentativa inválida de exclusão do personagem ID {id} pelo usuário {user_id}')
        flash('Personagem não encontrado ou você não tem permissão para excluí-lo.', 'danger')

    return redirect(url_for('main.dashboard'))