from app.db import DatabaseConnection
from app.models.user_model import Usuario

def inicializar_banco():
    with DatabaseConnection() as db:
        # Tabela de Usuário
        db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                regiao TEXT NOT NULL,
                senha_hash TEXT NOT NULL
            )
        ''')

        # Tabela de Personagem
        db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS personagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                elemento TEXT NOT NULL,
                arma TEXT NOT NULL,
                raridade INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        ''')

        # Tabela de Arma
        db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS armas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                raridade INTEGER NOT NULL,
                nivel INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
            )
        ''')

    # Usuário de teste inicial
    if not Usuario.buscar_por_uid('600123456'):
        usuario_teste = Usuario(
            username='Aether',
            uid='600123456',
            regiao='America',
            senha='1234'
        )
        usuario_teste.salvar()
        print("Usuário de teste inicial criado (UID: 600123456 | Senha: 1234).")

    print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    inicializar_banco()