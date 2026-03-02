import customtkinter as ctk
from logic import Login
from quary import Conexao
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import winsound
import time

# Configurações iniciais da janela
class configuracoesT:
    # Define o tema escuro e as dimensões iniciais da janela principal
    def __init__(self, dimençoes = "400x400"):
        janela = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.janela = ctk.CTk()
#        self.janela.iconbitmap("logo.ico")
        self.janela.geometry(dimençoes)
        self.janela.resizable(False, False)
        self.janela.title("Conta")
        
    def retornar_janela(self):
        return  self.janela
    
class persistencia_de_dados:
    # Gerencia a tela de Login e a transição para a tela do usuário
    def __init__(self, janela):
        self.janela = janela
        self.frame = None
        self.sistema = None
        
    def ao_clicar(self):
        # Ação do botão de login: valida os dados e carrega o painel do usuário se tudo estiver ok
        usuario_validado = self.sistema.validar_campos(self.nome_entry, self.senha_entry)
        
        if usuario_validado:
            db_server = Conexao(usuario_validado.nome, usuario_validado.senha)
            tela_usuarioT(frame=self.frame, janela=self.janela, nome_usuario=usuario_validado.nome, senha_usuario=usuario_validado.senha, id_usuario=usuario_validado.id, db_server=db_server).tela_config_usuario()  
         
            
            
    def controles(self):
        # Monta visualmente o formulário de login (campos, botões e labels)
        try:
            # Configuração de Cores (Pode ser movido para o __init__)
            primary_color = "#2563EB"  # Azul Moderno
            hover_color = "#1D4ED8"
            bg_secondary = "#1E1E1E" if ctk.get_appearance_mode() == "Dark" else "#F3F4F6"

            # Frame Principal Centralizado
            self.frame = ctk.CTkFrame(self.janela, corner_radius=24, fg_color=bg_secondary, border_width=1)
            self.frame.place(relx=0.5, rely=0.5, anchor="center") # Centralização perfeita

            # Título e Subtítulo
            self.titulo = ctk.CTkLabel(
                self.frame, 
                text="Bem-vindo de volta", 
                font=("Segoe UI", 28, "bold")
            )
            self.titulo.pack(pady=(40, 5), padx=50)

            self.subtitulo = ctk.CTkLabel(
                self.frame, 
                text="Entre com suas credenciais para acessar", 
                font=("Segoe UI", 13),
                text_color="gray"
            )
            self.subtitulo.pack(pady=(0, 30))

            # Campo: Usuário
            self.nome_entry = ctk.CTkEntry(
                self.frame, 
                placeholder_text="Nome de Usuário", 
                width=320, 
                height=50,
                border_width=2,
                corner_radius=10
            )
            self.nome_entry.pack(pady=12)

            # Campo: Senha
            self.senha_entry = ctk.CTkEntry(
                self.frame, 
                placeholder_text="Sua senha", 
                show="*", 
                width=320, 
                height=50,
                border_width=2,
                corner_radius=10
            )
            self.senha_entry.pack(pady=12)

            # Label de Erro (Elegante e discreta)
            self.erro_label = ctk.CTkLabel(
                self.frame, 
                text="", 
                text_color="#EF4444", 
                font=("Segoe UI", 12, "italic")
            )
            self.erro_label.pack(pady=(5, 0))
            
            # Inicialização do sistema de login
            self.sistema = Login(self.erro_label)        

            # Botão de Login Estilizado
            self.botao = ctk.CTkButton(
                self.frame, 
                text="Entrar no Sistema", 
                width=320, 
                height=50, 
                corner_radius=10,
                font=("Segoe UI", 15, "bold"),
                fg_color=primary_color,
                hover_color=hover_color,
                command=lambda: self.ao_clicar()
            )
            self.botao.pack(pady=(30, 40))
            
        except Exception as e:
            print(f"Erro ao carregar interface: {e}")
        
class tela_usuarioT:
    # Classe principal que gerencia todas as telas do painel do usuário (Timer, Home, Gráficos)
    def __init__(self, frame, janela, nome_usuario,senha_usuario,id_usuario,db_server):
        self.frame = frame
        self.janela = janela
        self.nome_usuario = nome_usuario
        self.senha_usuario = senha_usuario
        self.id = id_usuario
        self.conexao_DB = db_server
        self.after_id = None
        self.rodando = False

    def _parar_timer(self):
        # Interrompe a contagem do relógio e limpa agendamentos para evitar erros
        """Para o timer e cancela agendamentos pendentes de forma segura."""
        self.rodando = False
        if self.after_id:
            try:
                self.janela.after_cancel(self.after_id)
            except:
                pass
            self.after_id = None



    def comecar(self):
        # Monta a interface do Cronômetro (Timer) para o usuário focar

        # 2. Cancela qualquer processo de timer antigo (Crucial!)
        self._parar_timer()

        # 3. Limpeza Segura
        for widget in self.container_centro.winfo_children():
            widget.destroy()

        timer_card = ctk.CTkFrame(
            self.container_centro,
            width=750,        
            height=600,
            corner_radius=50,
            fg_color="#2b2b2b",
            border_width=1,
            border_color="#3D3D3D"
        )
        timer_card.place(relx=0.5, rely=0.5, anchor="center")
        timer_card.pack_propagate(False)

         
    # 3. Agora sim, chamamos a montagem do conteúdo do temporizador, que é a parte mais complexa 
        # --- CABEÇALHO ---
        ctk.CTkLabel(
            timer_card, 
            text="⏱ Temporizador de Foco", 
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        ).pack(pady=(40, 5))

        ctk.CTkLabel(
            timer_card, 
            text="Configure o tempo desejado e mantenha a concentração", 
            font=("Segoe UI", 14), 
            text_color="gray"
        ).pack(pady=(0, 20))


        # --- ÁREA DE INPUTS ---
        input_group = ctk.CTkFrame(timer_card, fg_color="#1e1e1e", corner_radius=15)
        input_group.pack(pady=10)
        
        input_frame = ctk.CTkFrame(input_group, fg_color="transparent")
        input_frame.pack(padx=30, pady=15)

        entry_h = ctk.CTkEntry(
            input_frame, width=80, height=45, placeholder_text="HH", 
            font=("Segoe UI", 20, "bold"), justify="center",
            fg_color="#0F172A", border_color="#3B82F6"
        )
        entry_h.grid(row=0, column=0)
        
        ctk.CTkLabel(input_frame, text=":", font=("Segoe UI", 26, "bold"), text_color="#3B82F6").grid(row=0, column=1, padx=10)
        
        entry_m = ctk.CTkEntry(
            input_frame, width=80, height=45, placeholder_text="MM", 
            font=("Segoe UI", 20, "bold"), justify="center",
            fg_color="#0F172A", border_color="#3B82F6"
        )
        entry_m.grid(row=0, column=2)

        # --- DISPLAY GIGANTE ---
        self.label_tempo = ctk.CTkLabel(
            timer_card,
            text="00:00:00",
            font=("Segoe UI", 130, "bold"), # Aumentado para preencher o centro do card
            text_color="#22c55e"
        )
        self.label_tempo.pack(expand=True)

        # --- VARIÁVEIS DE CONTROLE ---
        self.total_segundos = 0
        self.tempo_inicial = 0

        # --- FUNÇÕES DE LÓGICA ---
        def atualizar_display():
            h, resto = divmod(self.total_segundos, 3600)
            m, s = divmod(resto, 60)
            self.label_tempo.configure(text=f"{h:02d}:{m:02d}:{s:02d}")

        def contar():
            # Função recursiva que diminui o tempo a cada segundo e salva no banco ao terminar
            if not self.rodando:
                return
            try:
                if not self.label_tempo.winfo_exists():
                    self.rodando = False
                    return
            except:
                self.rodando = False
                return

            if self.rodando and self.total_segundos > 0:
                self.total_segundos -= 1
                atualizar_display()
                self.after_id = self.janela.after(1000, contar)
            elif self.total_segundos == 0 and self.rodando:
                self.label_tempo.configure(text="Concluído!", text_color="#3b82f6", font=("Segoe UI", 70, "bold"))
                self.rodando = False
                self.conexao_DB.salvar_historico(self.id, self.tempo_inicial)
                import winsound
                winsound.Beep(1000, 1000)

        def iniciar_timer():
            # Lê o input do usuário e começa a contagem regressiva
            if not self.rodando:
                if self.total_segundos == 0:
                    try:
                        h = int(entry_h.get() or 0)
                        m = int(entry_m.get() or 0)
                        self.total_segundos = (h * 3600) + (m * 60)
                        self.tempo_inicial = self.total_segundos
                    except ValueError: return
                
                if self.total_segundos > 0:
                    self.rodando = True
                    self.label_tempo.configure(text_color="#22c55e", font=("Segoe UI", 130, "bold"))
                    contar()

        def pausar_timer():
            # Congela o tempo atual sem resetar
            self.rodando = False
            if self.after_id:
                self.janela.after_cancel(self.after_id)

        def resetar_timer():
            # Zera o cronômetro e permite inserir um novo tempo
            pausar_timer()
            self.total_segundos = 0
            self.label_tempo.configure(text_color="#22c55e", font=("Segoe UI", 130, "bold"))
            atualizar_display()

# --- BOTÕES DE AÇÃO (Iniciar e Pausar) ---
        button_frame = ctk.CTkFrame(timer_card, fg_color="transparent")
        button_frame.pack(pady=(10, 20)) # Espaço acima e abaixo do grupo principal

        btn_start = ctk.CTkButton(
            button_frame, text="▶ Iniciar", width=140, height=45,
            fg_color="#22c55e", hover_color="#16a34a", font=("Segoe UI", 14, "bold"),
            command=iniciar_timer
        )
        btn_start.grid(row=0, column=0, padx=10)

        btn_pause = ctk.CTkButton(
            button_frame, text="⏸ Pausar", width=140, height=45,
            fg_color="#f59e0b", hover_color="#d97706", font=("Segoe UI", 14, "bold"),
            command=pausar_timer
        )
        btn_pause.grid(row=0, column=1, padx=10)

        # --- BOTÃO RESETAR (Corrigido para não ficar espremido) ---
        # Aumentamos o pady superior para criar uma separação clara
        btn_reset = ctk.CTkButton(
            timer_card, 
            text="🔄 Resetar Temporizador", 
            width=250,                  # Aumentado para ter mais presença
            height=40,                  # Altura confortável
            fg_color="transparent", 
            border_width=1, 
            border_color="#3d3d3d",
            text_color="#94A3B8", 
            hover_color="#334155",
            command=resetar_timer, 
            font=("Segoe UI", 13)
        )
        # O segredo: pady=(30, 40) empurra ele 30px para longe dos botões de cima 
        # e garante 40px de margem do fundo do card
        btn_reset.pack(pady=(10, 40))

    def mostrar_home(self):
        # Exibe o painel inicial com resumo do dia (tempo estudado, meta e status)
        self._parar_timer()
    # 1. Limpeza da área central
        for widget in self.container_centro.winfo_children():
            widget.destroy()

        # 2. Cores da sua Paleta
        bg_color = "#0F172A" 
        side_color = "#2b2b2b"
        accent_color = "#3B82F6"
        
        # 3. Obtenção dos dados tratados
        tempo, meta_porcent, status, msg, cor_status = self.obter_dados_resumo()

        # 4. Cabeçalho
        header_frame = ctk.CTkFrame(self.container_centro, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))

        ctk.CTkLabel(
            header_frame, 
            text=f"Bem-vindo, {self.nome_usuario} 👋", 
            font=("Segoe UI", 32, "bold"), 
            text_color="white",
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            header_frame, 
            text="Aqui está o resumo do seu desempenho acadêmico de hoje.", 
            font=("Segoe UI", 14), 
            text_color="#64748B", 
            anchor="w"
        ).pack(fill="x")

        # 5. Container de Cards
        summary_container = ctk.CTkFrame(self.container_centro, fg_color="transparent")
        summary_container.pack(fill="x", pady=(0, 20))

        def criar_card(titulo, valor, icone, cor_valor):
            card = ctk.CTkFrame(
                summary_container, 
                fg_color=side_color, 
                corner_radius=15, 
                border_width=1, 
                border_color="#3D3D3D"
            )
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            ctk.CTkLabel(
                card, text=f"{icone} {titulo}", 
                font=("Segoe UI", 12, "bold"), 
                text_color="#94A3B8"
            ).pack(pady=(15, 0), padx=20, anchor="w")
            
            ctk.CTkLabel(
                card, text=valor, 
                font=("Segoe UI", 28, "bold"), 
                text_color=cor_valor
            ).pack(pady=(5, 15), padx=20, anchor="w")

        # Renderização dos Cards com os dados dinâmicos
        criar_card("Tempo Estudado", tempo, "⏱", accent_color)
        criar_card("Meta Diária", meta_porcent, "🎯", "#10B981")
        criar_card("Status Atual", status, "🔥", cor_status)

        # 6. Card de Feedback Motivacional (Preenche o resto da tela)
        footer_card = ctk.CTkFrame(
            self.container_centro, 
            fg_color=side_color, 
            corner_radius=15, 
            border_width=1, 
            border_color="#3D3D3D"
        )
        footer_card.pack(fill="both", expand=True, pady=10)

        # Emoji grande para dar um toque visual
        ctk.CTkLabel(
            footer_card, 
            text="✨", 
            font=("Segoe UI", 50)
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            footer_card, 
            text=msg, 
            font=("Segoe UI", 18, "italic"), 
            text_color="white",
            wraplength=600 # Evita que o texto saia da tela se for longo
        ).pack(pady=(0, 60))
        
    def mostrar_grafico(self):
        # Gera e exibe um gráfico de barras com o histórico de estudo usando Matplotlib
        self._parar_timer()
        # 1. Limpeza do Container
        for widget in self.container_centro.winfo_children():
            widget.destroy()

        # Configurações Visuais (Design System)
        bg_color = "#0F172A"      # Azul Marinho Profundo
        card_color = "#1E293B"    # Slate
        accent_blue = "#3B82F6"
        success_green = "#10B981"
        error_red = "#F87171"
        text_main = "#F8FAFC"
        text_secondary = "#94A3B8"

        # Busca de dados no Banco
        dados = self.conexao_DB.buscar_dados_diarios(self.id)
        meta = self.conexao_DB.buscar_meta(self.id)

        if not dados:
            ctk.CTkLabel(
                self.container_centro,
                text="🧐 Sem dados para análise ainda.\nInicie um cronômetro para ver seu progresso!",
                font=("Segoe UI", 18),
                text_color=text_secondary
            ).pack(pady=100)
            return

        # 2. Cabeçalho
        header_frame = ctk.CTkFrame(self.container_centro, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(header_frame, text="📊 Análise de Performance", 
                    font=("Segoe UI", 28, "bold"), text_color=text_main, anchor="w").pack(fill="x")

        # 3. Preparação dos Dados
        datas, valores_segundos, labels_formatados, cores = [], [], [], []

        for data, segundos in dados:
            data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m")
            datas.append(data_formatada)
            valores_segundos.append(segundos)
            
            # Formatação para o texto acima das barras
            h, m = segundos // 3600, (segundos % 3600) // 60
            if h > 0:
                labels_formatados.append(f"{h}h {m}m" if m > 0 else f"{h}h")
            else:
                labels_formatados.append(f"{m}m")
            
            cores.append(success_green if segundos >= meta else accent_blue)

        # 4. Configuração do Matplotlib
        plt.rcParams['font.family'] = 'Segoe UI'
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        barras = ax.bar(datas, valores_segundos, color=cores, alpha=0.8, width=0.6)

        # Linha da Meta
        ax.axhline(meta, color=error_red, linestyle="--", linewidth=1.5, alpha=0.7, label="Sua Meta")
        
        # --- FUNÇÃO DE FORMATAÇÃO DO EIXO Y (SEM 0h) ---
        def formatar_tempo_eixo(valor, pos):
            if valor <= 0: return "0"
            h = int(valor // 3600)
            m = int((valor % 3600) // 60)
            s = int(valor % 60)

            if h > 0:
                return f"{h}h" if m == 0 else f"{h}h{m:02d}m"
            elif m > 0:
                return f"{m}m"
            else:
                return f"{s}s"

        ax.yaxis.set_major_formatter(FuncFormatter(formatar_tempo_eixo))

        # --- CÁLCULO DAS 10 ETAPAS ---
        import numpy as np
        valor_base = max(meta, max(valores_segundos) if valores_segundos else meta)
        limite_superior = valor_base * 1.15  # 15% de folga no topo
        
        # np.linspace gera 11 pontos para criar exatamente 10 espaços/etapas
        etapas = np.linspace(0, limite_superior, 11)
        ax.set_yticks(etapas)

        # Estética dos Eixos
        ax.tick_params(axis='both', colors=text_secondary, labelsize=9)
        ax.spines['bottom'].set_color(card_color)
        ax.spines['left'].set_color(card_color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Grade Suave
        ax.yaxis.grid(True, linestyle='--', alpha=0.1, color=text_main)
        ax.set_axisbelow(True)

        # Texto acima das barras (Porcentagem e Tempo)
        for i, barra in enumerate(barras):
            porcentagem = (valores_segundos[i] / meta) * 100 if meta > 0 else 0
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + (limite_superior * 0.02),
                f"{labels_formatados[i]}\n{porcentagem:.0f}%",
                ha='center', va='bottom', color=text_main, fontsize=8, fontweight='bold'
            )

        fig.tight_layout()

        # 5. Integração Final com CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.container_centro)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(background=bg_color)
        canvas_widget.pack(fill="both", expand=True, pady=10)

    def tela_meta(self):
        # Tela de configuração onde o usuário define sua meta diária de horas
        self._parar_timer()
        # Limpa o conteúdo anterior
        for widget in self.container_centro.winfo_children():
            widget.destroy()

        # Título e Subtítulo da Seção
        header_frame = ctk.CTkFrame(self.container_centro, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 40))

        ctk.CTkLabel(
            header_frame, 
            text="🎯 Definir Meta Diária", 
            font=("Segoe UI", 28, "bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            header_frame, 
            text="Estabeleça quanto tempo você deseja focar hoje.", 
            font=("Segoe UI", 14),
            text_color="#94A3B8",
            anchor="w"
        ).pack(fill="x")

        # Card Centralizado (Formulário)
        card_meta = ctk.CTkFrame(self.container_centro, fg_color="#1e1e1e", corner_radius=15, border_width=1, border_color="#2b2b2b")
        card_meta.pack(pady=10, padx=2, ipadx=20, ipady=20)

        # Container para os inputs lado a lado
        input_group = ctk.CTkFrame(card_meta, fg_color="transparent")
        input_group.pack(pady=(20, 10))

        # Coluna Horas
        col_h = ctk.CTkFrame(input_group, fg_color="transparent")
        col_h.grid(row=0, column=0, padx=15)
        ctk.CTkLabel(col_h, text="Horas", font=("Segoe UI", 12, "bold"), text_color="#64748B").pack()
        entry_h = ctk.CTkEntry(col_h, width=100, height=45, placeholder_text="00", justify="center", font=("Segoe UI", 16))
        entry_h.pack(pady=5)

        # Coluna Minutos
        col_m = ctk.CTkFrame(input_group, fg_color="transparent")
        col_m.grid(row=0, column=1, padx=15)
        ctk.CTkLabel(col_m, text="Minutos", font=("Segoe UI", 12, "bold"), text_color="#64748B").pack()
        entry_m = ctk.CTkEntry(col_m, width=100, height=45, placeholder_text="00", justify="center", font=("Segoe UI", 16))
        entry_m.pack(pady=5)

        # Label de Status (Erro/Sucesso)
        self.status_meta = ctk.CTkLabel(card_meta, text="", font=("Segoe UI", 12))
        self.status_meta.pack(pady=5)

        def salvar():
            # Valida os inputs e salva a nova meta no banco de dados
            try:
                h = entry_h.get().strip()
                m = entry_m.get().strip()
                
                horas = int(h if h else 0)
                minutos = int(m if m else 0)

                if horas == 0 and minutos == 0:
                    raise ValueError("Defina um tempo maior que zero")

                total_segundos = horas * 3600 + minutos * 60
                self.conexao_DB.atualizar_meta(self.id, total_segundos)

                self.status_meta.configure(text="✅ Meta salva com sucesso!", text_color="#10B981")
                # Limpa a mensagem após 3 segundos
                self.janela.after(3000, lambda: self.status_meta.configure(text="") if self.status_meta.winfo_exists() else None)

            except ValueError as e:
                self.status_meta.configure(text="❌ Insira valores válidos", text_color="#F87171")
                self.janela.after(3000, lambda: self.status_meta.configure(text=""))

        # Botão Salvar (Largo e com cor de destaque)
        btn_salvar = ctk.CTkButton(
            card_meta,
            text="Confirmar Meta",
            height=45,
            width=230,
            font=("Segoe UI", 14, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=salvar
        )
        btn_salvar.pack(pady=(10, 20))

    def obter_dados_resumo(self):
        # Calcula as estatísticas do dia atual para preencher os cards da Home
        # 1. Busca dados de hoje e calcula total de segundos
        dados_brutos = self.conexao_DB.buscar_dados_diarios(self.id)
        total_segundos_hoje = sum(segundos for data, segundos in dados_brutos)
        
        # 2. Formata tempo para o card "Hoje"
        horas = total_segundos_hoje // 3600
        minutos = (total_segundos_hoje % 3600) // 60
        tempo_hoje_str = f"{horas:02d}h {minutos:02d}m"
        
        # 3. Busca meta e calcula porcentagem
        meta_segundos = self.conexao_DB.buscar_meta(self.id)
        porcentagem = 0
        if meta_segundos > 0:
            porcentagem = min(int((total_segundos_hoje / meta_segundos) * 100), 100)
        
        meta_str = f"{porcentagem}%"

        # 4. Lógica de Comentários Variados (Feedback Motivacional)
        if total_segundos_hoje == 0:
            status_str, cor_status = "Pausado", "#94A3B8"
            comentario = "Que tal começar a primeira sessão de hoje? 🚀"
        elif porcentagem < 100:
            status_str, cor_status = "Focado", "#F59E0B"
            comentario = "Continue assim! A meta está logo ali. 🌱"
        else:
            status_str, cor_status = "Concluído", "#10B981"
            comentario = "Meta batida! Você foi excelente hoje. 🏆"
                
        return tempo_hoje_str, meta_str, status_str, comentario, cor_status
#"#2b2b2b"
    def tela_config_usuario(self):
        # Configura o layout principal pós-login: Sidebar à esquerda e Conteúdo à direita
        self.frame.destroy()
        self.janela.geometry("1100x600")
        
        # Sua Paleta Original Restaurada
        bg_color = "#0F172A" 
        side_color = "#2b2b2b"
        accent_color = "#3B82F6"
        hover_color = "#334155"

        self.janela.configure(fg_color=bg_color)

        # Configuração da Grade Principal
        self.janela.grid_columnconfigure(0, weight=0)
        self.janela.grid_columnconfigure(1, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        sidebar = ctk.CTkFrame(self.janela, width=260, corner_radius=0, fg_color=side_color, border_width=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # 1. Perfil do Usuário
        profile_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        profile_frame.pack(pady=(40, 20), padx=20, fill="x")

        ctk.CTkLabel(
            profile_frame, 
            text="🎓", 
            font=("Segoe UI", 22),
            width=45, height=45,
            fg_color=hover_color, # Usando sua cor de hover para o fundo do ícone
            corner_radius=12
        ).pack(side="left", padx=(0, 12))
        
        user_text_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        user_text_frame.pack(side="left")

        ctk.CTkLabel(user_text_frame, text=self.nome_usuario, font=("Segoe UI", 15, "bold"), anchor="w").pack(fill="x")
        ctk.CTkLabel(user_text_frame, text="● Online", font=("Segoe UI", 11), text_color="#10B981", anchor="w").pack(fill="x")

        # Separador
        ctk.CTkFrame(sidebar, height=2, fg_color="#3D3D3D").pack(padx=20, fill="x", pady=15)

        # 2. Navegação
        nav_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_container.pack(fill="both", expand=True, padx=15)

        def criar_botao_menu(texto, icone, comando):
            btn = ctk.CTkButton(
                nav_container,
                text=f"  {icone}   {texto}",
                font=("Segoe UI", 13),
                anchor="w",
                height=45,
                corner_radius=8,
                fg_color="transparent",
                text_color="#94A3B8",
                hover_color=hover_color,
                command=comando
            )
            btn.pack(pady=4, fill="x")
            return btn
        
        self.btn_home = criar_botao_menu("Home", "🏠", self.mostrar_home)
        self.btn_dash = criar_botao_menu("Análise", "📊", self.mostrar_grafico)
        self.btn_comecar = criar_botao_menu("Começar", "⏱", self.comecar)
        self.btn_meta = criar_botao_menu("Definir Meta", "🎯", self.tela_meta)

        # Rodapé Sair
        ctk.CTkButton(
            sidebar, text="🚪 Sair do Sistema", 
            font=("Segoe UI", 12),
            fg_color="transparent", text_color="#F87171",
            hover_color="#450a0a",
            command=lambda: self.janela.destroy()
        ).pack(side="bottom", pady=20, padx=20, fill="x")

        # --- ÁREA DE CONTEÚDO (DIREITA) ---
        self.container_centro = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.container_centro.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Cabeçalho de Boas-vindas
        ctk.CTkLabel(self.container_centro, text=f"Olá, {self.nome_usuario} 👋", font=("Segoe UI", 32, "bold"), anchor="w").pack(fill="x")
        ctk.CTkLabel(self.container_centro, text="Seja bem-vindo ao seu painel de controle.", font=("Segoe UI", 14), text_color="#64748B", anchor="w").pack(fill="x", pady=(0, 40))

        # --- CARDS PARA PREENCHER O ESPAÇO VAZIO ---
        summary_container = ctk.CTkFrame(self.container_centro, fg_color="transparent")
        summary_container.pack(fill="x", pady=(0, 20))

        def criar_card(titulo, valor, icone, cor_texto):
            # Card usando a cor da sidebar para manter a harmonia do seu design
            card = ctk.CTkFrame(summary_container, fg_color=side_color, corner_radius=15, border_width=1, border_color="#3D3D3D")
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            ctk.CTkLabel(card, text=f"{icone} {titulo}", font=("Segoe UI", 12, "bold"), text_color="#94A3B8").pack(pady=(15, 0), padx=15, anchor="w")
            ctk.CTkLabel(card, text=valor, font=("Segoe UI", 26, "bold"), text_color=cor_texto).pack(pady=(5, 15), padx=15, anchor="w")
