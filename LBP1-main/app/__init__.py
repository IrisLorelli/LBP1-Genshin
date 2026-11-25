import os
from flask import Flask, render_template
from iniciar_bd import inicializar_banco

def create_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.secret_key = 'genshin_secret_key_spolbp1'

    # Inicializa tabelas
    inicializar_banco()

    # Registro de Blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.personagem_controller import personagem_bp
    from app.controllers.arma_controller import arma_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(personagem_bp)
    app.register_blueprint(arma_bp)

    # Tratamento de erro 404
    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        app.logger.warning(f'Página não encontrada (404): {erro}')
        return render_template('404.html'), 404

    return app