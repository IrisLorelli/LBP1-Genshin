from app.db import DatabaseConnection

class Personagem:
    def __init__(self, usuario_id, nome, elemento, arma, raridade, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.nome = nome
        self.elemento = elemento
        self.arma = arma
        self.raridade = raridade

    def salvar(self):
        """Insere o personagem associado ao ID do usuário autenticado."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                INSERT INTO personagens (usuario_id, nome, elemento, arma, raridade)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.usuario_id, self.nome, self.elemento, self.arma, self.raridade))
            self.id = db.cursor.lastrowid

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        """Retorna todos os personagens cadastrados pelo usuário."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                SELECT id, usuario_id, nome, elemento, arma, raridade
                FROM personagens
                WHERE usuario_id = ?
                ORDER BY id DESC
            ''', (usuario_id,))
            linhas = db.cursor.fetchall()

        return [
            cls(
                id=linha['id'],
                usuario_id=linha['usuario_id'],
                nome=linha['nome'],
                elemento=linha['elemento'],
                arma=linha['arma'],
                raridade=linha['raridade']
            )
            for linha in linhas
        ]

    @classmethod
    def buscar_por_id(cls, personagem_id, usuario_id):
        """Busca um personagem específico validando o dono."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                SELECT id, usuario_id, nome, elemento, arma, raridade
                FROM personagens
                WHERE id = ? AND usuario_id = ?
            ''', (personagem_id, usuario_id))
            linha = db.cursor.fetchone()

        if linha:
            return cls(
                id=linha['id'],
                usuario_id=linha['usuario_id'],
                nome=linha['nome'],
                elemento=linha['elemento'],
                arma=linha['arma'],
                raridade=linha['raridade']
            )
        return None

    @classmethod
    def excluir(cls, personagem_id, usuario_id):
        """Exclui o personagem apenas se pertencer ao usuário logado."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                DELETE FROM personagens
                WHERE id = ? AND usuario_id = ?
            ''', (personagem_id, usuario_id))
            return db.cursor.rowcount > 0