from app.db import DatabaseConnection

class Arma:
    def __init__(self, usuario_id, nome, tipo, raridade, nivel, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.nome = nome
        self.tipo = tipo
        self.raridade = raridade
        self.nivel = nivel

    def salvar(self):
        """Insere uma nova arma associada ao ID do usuário autenticado."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                INSERT INTO armas (usuario_id, nome, tipo, raridade, nivel)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.usuario_id, self.nome, self.tipo, self.raridade, self.nivel))
            self.id = db.cursor.lastrowid

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        """Retorna todas as armas cadastradas pelo usuário."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                SELECT id, usuario_id, nome, tipo, raridade, nivel
                FROM armas
                WHERE usuario_id = ?
                ORDER BY id DESC
            ''', (usuario_id,))
            linhas = db.cursor.fetchall()

        return [
            cls(
                id=linha['id'],
                usuario_id=linha['usuario_id'],
                nome=linha['nome'],
                tipo=linha['tipo'],
                raridade=linha['raridade'],
                nivel=linha['nivel']
            )
            for linha in linhas
        ]

    @classmethod
    def buscar_por_id(cls, arma_id, usuario_id):
        """Busca uma arma específica validando o dono."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                SELECT id, usuario_id, nome, tipo, raridade, nivel
                FROM armas
                WHERE id = ? AND usuario_id = ?
            ''', (arma_id, usuario_id))
            linha = db.cursor.fetchone()

        if linha:
            return cls(
                id=linha['id'],
                usuario_id=linha['usuario_id'],
                nome=linha['nome'],
                tipo=linha['tipo'],
                raridade=linha['raridade'],
                nivel=linha['nivel']
            )
        return None

    @classmethod
    def excluir(cls, arma_id, usuario_id):
        """Exclui a arma apenas se pertencer ao usuário logado."""
        with DatabaseConnection() as db:
            db.cursor.execute('''
                DELETE FROM armas
                WHERE id = ? AND usuario_id = ?
            ''', (arma_id, usuario_id))
            return db.cursor.rowcount > 0