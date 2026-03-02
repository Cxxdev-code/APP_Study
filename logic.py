from quary import Conexao
import hashlib
from time import sleep
# classe de login e logica
class Usuario:
    # Modelo de dados do usuário que cuida da segurança da senha automaticamente
    def __init__(self,):
        self._nome = None
        self._senha = None
        self._id = None
        self._senha = None 


    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome):
        self._nome = nome
        
    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, senha_plana):
        # Transforma a senha digitada em um hash seguro (SHA-256) antes de salvar
        # Gerando o hash SHA-256 da senha
        sha256 = hashlib.sha256()
        sha256.update(senha_plana.encode('utf-8'))
        self._senha = sha256.hexdigest()

        
class Login:
    # Controla as regras de validação e o fluxo de entrada no sistema
    def __init__(self, erro_label):
        self.erro_label = erro_label
        self.usuario = Usuario()
        
        
    def sanitizar_nome(self, nome):
        # Remove espaços extras desnecessários do nome
        nome_limpo = " ".join(nome.split())
        return nome_limpo
    
    
    def validar_nome(self, nome):
        # Garante que o nome tenha pelo menos 5 letras e não contenha símbolos estranhos

        if len(nome) < 5:
            return False
        
        if not all(c.isalpha() or c.isspace() for c in nome):
            return False

        return True

    def validar_senha(self, senha):
        # Verifica se a senha atende ao tamanho mínimo exigido
        if len(senha) < 5:
            return False

        return True
    
    def validar_campos(self, nome_entry, senha_entry):
        # Processa a tentativa de login: valida, conecta no banco e dá feedback visual
        nome_bruto = nome_entry.get()
        nome_pronto = self.sanitizar_nome(nome_bruto)
        senha = senha_entry.get()

        # 1. Validações de Formato (UX: Feedback em vermelho)
        if not self.validar_nome(nome_pronto):
            self.erro_label.configure(text="Nome inválido (mín. 5 letras)", text_color="#EF4444")
            return

        if not self.validar_senha(senha):
            self.erro_label.configure(text="Senha inválida (mín. 5 caracteres)", text_color="#EF4444")
            return

        # 2. Lógica de Banco de Dados
        self.usuario.nome = nome_pronto
        self.usuario.senha = senha
        
        conn = Conexao(self.usuario.nome, self.usuario.senha)
        
        # Aqui recebemos o ID e a confirmação se é novo
        id_usuario, conta_criada = conn.buscar_ou_criar_usuario()
        
        self.usuario.id = id_usuario
        
        if conta_criada:
            self.erro_label.configure(
                text="Conta criada com sucesso!",
                text_color="#3B82F6" # Azul (Info) combina melhor com o tema Dark/Moderno
            )
        else:
            self.erro_label.configure(
                text="Login realizado!",
                text_color="#10B981" # Verde (Sucesso)
            )
        nome_entry.update()
        
        sleep(0.9)  # Pequena pausa para o usuário ler a mensagem
            
        return self.usuario
        
