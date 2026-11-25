from werkzeug.security import generate_password_hash, check_password_hash
from app.db import DatabaseConnection

class Usuario:
    def __init__(self, username, uid, regiao, senha=None, senha_hash=None, id=None):
        self.id = id
        self.username = username
        self.uid = uid
        self.regiao = regiao
        self.senha_hash = generate_password_hash(senha) if senha else senha_hash

    def verificar_senha(self, senha):
        """Compara a senha digitada com o hash armazenado no banco."""
        if not self.senha_hash:
            return False
        return check_password_hash(self.senha_hash, senha)

    def salvar(self):
        """Insere um novo usuário no banco com senha criptografada."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                INSERT INTO usuarios (uid, username, regiao, senha_hash)
                VALUES (?, ?, ?, ?)
            ''', (self.uid, self.username, self.regiao, self.senha_hash))
            self.id = db.cursor.lastrowid

    @classmethod
    def buscar_por_id(cls, user_id):
        """Busca usuário pela chave primária (usado pelo middleware)."""
        with DatabaseConnection() as db:
            db.cursor.execute(
                'SELECT id, uid, username, regiao, senha_hash FROM usuarios WHERE id = ?',
                (user_id,)
            )
            linha = db.cursor.fetchone()

        if linha:
            return cls(
                id=linha['id'],
                uid=linha['uid'],
                username=linha['username'],
                regiao=linha['regiao'],
                senha_hash=linha['senha_hash']
            )
        return None

    @classmethod
    def buscar_por_uid(cls, uid):
        """Busca usuário pelo UID do jogo (usado no login e validação de cadastro)."""
        with DatabaseConnection() as db:
            db.cursor.execute(
                'SELECT id, uid, username, regiao, senha_hash FROM usuarios WHERE uid = ?',
                (uid,)
            )
            linha = db.cursor.fetchone()

        if linha:
            return cls(
                id=linha['id'],
                uid=linha['uid'],
                username=linha['username'],
                regiao=linha['regiao'],
                senha_hash=linha['senha_hash']
            )
        return None