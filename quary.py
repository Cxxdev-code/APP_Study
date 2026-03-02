import sqlite3
from datetime import date
import os
import sys

def get_data_path(filename):
    # Descobre o caminho correto do arquivo, funcionando tanto no script quanto no executável (.exe)
    """
    Retorna o caminho absoluto para um arquivo de dados (como o DB),
    garantindo que ele fique ao lado do .exe ou do script.
    """
    if getattr(sys, 'frozen', False):
        # O aplicativo está "congelado" (executável).
        # O caminho base é o diretório onde o .exe está.
        base_path = os.path.dirname(sys.executable)
    else:
        # O aplicativo está rodando como um script .py.
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

BANCO = get_data_path("user.db")


    
def criar_tabelas():
    # Conecta ao banco e cria as tabelas essenciais (usuários e histórico) se elas não existirem
    with sqlite3.connect(BANCO) as conn:
        cursor = conn.cursor()

        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                meta_diaria INTEGER DEFAULT 7200
            )
        """)

        # Tabela de histórico
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_estudo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                tempo_segundos INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES usuarios(id)
            )
        """)

        conn.commit()

# adicionar usuario
class Conexao:
    # Gerencia todas as interações com o banco de dados para um usuário específico
    def __init__(self, nome, senha):
        self._nome = nome
        self._senha = senha
        
    def buscar_ou_criar_usuario(self):
        # Tenta achar o usuário; se não existir, cria uma conta nova automaticamente
        with sqlite3.connect(BANCO) as conn:
            cursor = conn.cursor()

            # Busca se o usuário existe com essa senha
            cursor.execute("""
                SELECT id FROM usuarios
                WHERE nome = ? AND senha = ?
            """, (self._nome, self._senha))

            usuario = cursor.fetchone()

            if usuario:
                # Retorna o ID e False (pois não é uma conta nova)
                return usuario[0], False

            # Se não existe, cria a conta
            cursor.execute("""
                INSERT INTO usuarios (nome, senha)
                VALUES (?, ?)
            """, (self._nome, self._senha))

            conn.commit()

        # Retorna o novo ID e True (pois a conta foi criada agora)
            return cursor.lastrowid, True

    def salvar_historico(self,user_id, tempo_segundos):
        # Registra o tempo estudado na data de hoje na tabela de histórico
        data_hoje = date.today().isoformat()

        with sqlite3.connect(BANCO) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO historico_estudo (user_id, data, tempo_segundos)
                VALUES (?, ?, ?)
            """, (user_id, data_hoje, tempo_segundos))

            conn.commit()
            
    def buscar_dados_diarios(self,user_id):
        # Agrupa e soma o tempo de estudo por dia para gerar o gráfico de desempenho
        with sqlite3.connect(BANCO) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT data, SUM(tempo_segundos)
                FROM historico_estudo
                WHERE user_id = ?
                GROUP BY data
                ORDER BY data
            """, (user_id,))

            return cursor.fetchall()

    def buscar_meta(self,user_id):
        # Recupera a meta diária definida pelo usuário (ou o padrão)
        with sqlite3.connect(BANCO) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT meta_diaria
                FROM usuarios
                WHERE id = ?
            """, (user_id,))

            return cursor.fetchone()[0]
        
    def atualizar_meta(self,user_id, nova_meta_segundos):
        # Atualiza o valor da meta diária de estudo no perfil do usuário
        with sqlite3.connect(BANCO) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuarios
                SET meta_diaria = ?
                WHERE id = ?
            """, (nova_meta_segundos, user_id))

            conn.commit()
            
    def apagar_tudo_mesmo(self):
        # Cuidado: Apaga todos os dados de todas as tabelas e reseta os IDs (uso administrativo)
        try:
            cursor = self.conexao.cursor()
            
            # Lista de todas as suas tabelas
            tabelas = ['usuarios', 'historico', 'metas']
            
            for tabela in tabelas:
                cursor.execute(f"DELETE FROM {tabela}")
                # Reseta o contador de ID de cada tabela
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabela}'")
                
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao apagar banco completo: {e}")
            return False

if __name__ == "__main__":
    conn = Conexao("test_user", "test_pass")
    criar_tabelas()
