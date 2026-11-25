from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
from app.models.user_model import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def root():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Recupera o último UID salvo no cookie do navegador
    ultimo_uid = request.cookies.get('ultimo_uid', '')

    if request.method == 'POST':
        acao = request.form.get('acao')  
        username = request.form.get('username', '').strip()
        uid = request.form.get('uid', '').strip()
        regiao = request.form.get('regiao', '').strip()
        senha = request.form.get('senha', '')

        # Validação básica servidor
        if not uid or not senha:
            flash('UID e senha são obrigatórios!', 'danger')
            return render_template('auth/login.html', ultimo_uid=uid)

        if len(senha) < 4:
            flash('A senha deve ter pelo menos 4 caracteres.', 'danger')
            return render_template('auth/login.html', ultimo_uid=uid)

        if acao == 'cadastrar':
            if not username or not regiao:
                flash('Preencha o nome de usuário e a região para criar a conta.', 'danger')
                return render_template('auth/login.html', ultimo_uid=uid)

            if len(username) < 2:
                flash('O nome de usuário deve ter pelo menos 2 caracteres.', 'danger')
                return render_template('auth/login.html', ultimo_uid=uid)

            usuario_existente = Usuario.buscar_por_uid(uid)
            if usuario_existente:
                current_app.logger.warning(f'Tentativa de cadastro com UID já existente: {uid}')
                flash('Este UID já está cadastrado no sistema!', 'danger')
            else:
                novo_usuario = Usuario(username=username, uid=uid, regiao=regiao, senha=senha)
                novo_usuario.salvar()

                # Busca o usuário recém-salvo -> id gerado no banco
                usuario_criado = Usuario.buscar_por_uid(uid)
                session.clear()
                session['user_id'] = usuario_criado.id
                session['username'] = usuario_criado.username
                session['usuario_uid'] = usuario_criado.uid
                session['regiao'] = usuario_criado.regiao

                current_app.logger.info(f'Novo usuário cadastrado: {username} (UID: {uid})')
                flash('Conta criada com sucesso! Bem-vindo(a), Viajante!', 'success')

                resposta = make_response(redirect(url_for('main.dashboard')))
                resposta.set_cookie('ultimo_uid', uid, max_age=60 * 60 * 24 * 30)  
                return resposta

        elif acao == 'entrar':
            usuario = Usuario.buscar_por_uid(uid)
            if usuario and usuario.verificar_senha(senha):
                session.clear()
                session['user_id'] = usuario.id
                session['username'] = usuario.username
                session['usuario_uid'] = usuario.uid
                session['regiao'] = usuario.regiao

                current_app.logger.info(f'Login realizado com sucesso: {usuario.username} (ID: {usuario.id})')
                flash(f'Bem-vindo(a) de volta, {usuario.username}!', 'success')

                resposta = make_response(redirect(url_for('main.dashboard')))
                resposta.set_cookie('ultimo_uid', uid, max_age=60 * 60 * 24 * 30)
                return resposta
            else:
                current_app.logger.warning(f'Falha de autenticação para o UID: {uid}')
                flash('UID ou senha incorretos!', 'danger')

    return render_template('auth/login.html', ultimo_uid=ultimo_uid)

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'Desconhecido')
    session.clear()
    current_app.logger.info(f'Logout realizado pelo usuário: {username}')
    flash('Você saiu da sua conta com segurança.', 'info')
    return redirect(url_for('auth.login'))