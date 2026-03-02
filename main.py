
from ui_commponents import configuracoesT, persistencia_de_dados
from quary import criar_tabelas

if __name__ == "__main__":
    # Ponto de entrada: Inicializa o banco, configura a janela e inicia o loop da interface
    # Garante que o arquivo .db e as tabelas existam antes de iniciar a UI
    criar_tabelas()
    config = configuracoesT()
    janela = config.retornar_janela()
    persistencia = persistencia_de_dados(janela)
    persistencia.controles()
    janela.mainloop()
