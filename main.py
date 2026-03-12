import customtkinter as ctk
import json
import os

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Arquivo de configuração de preços
CONFIG_FILE = "precos_config.json"

# Preços padrão
PRECOS_PADRAO = {
    "pb_unitario": 2.00,
    "pb_de_10": 0.50,
    "pb_de_30": 0.30,
    "pb_de_100": 0.25,
    "colorida_unitario": 2.00,
    "colorida_de_10": 1.50
}

class AppPapelaria(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Impressão")
        self.geometry("500x680")
        self.resizable(False, False)
        
        # Configurar janela em tela cheia confortável
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Carregar preços
        self.precos = self.carregar_precos(forcar_padrao=True)

        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # HEADER - Topo moderno
        self.criar_header(main_frame)

        # CONTEÚDO CENTRAL
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        content_frame.grid_columnconfigure(0, weight=1)

        self.criar_conteudo(content_frame)

        # FOOTER - Botões inferiores
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        footer_frame.grid_columnconfigure((0, 1), weight=1)

        self.criar_footer(footer_frame)

    def criar_header(self, parent):
        """Cabeçalho moderno e limpo"""
        header = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", pady=0)
        
        titulo = ctk.CTkLabel(
            header,
            text="🖨️  CALCULADORA DE IMPRESSÃO",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        titulo.pack(pady=25)

    def criar_conteudo(self, parent):
        """Conteúdo principal com layout limpo"""
        # Input de Quantidade
        label_qtd = ctk.CTkLabel(
            parent,
            text="Quantas páginas?",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#b0b0b0"
        )
        label_qtd.pack(anchor="w", pady=(0, 12))

        self.entry_qtd = ctk.CTkEntry(
            parent,
            placeholder_text="Digite o número de páginas...",
            height=60,
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#2a2a2a",
            border_color="#0099ff",
            border_width=2,
            corner_radius=12
        )
        self.entry_qtd.pack(fill="x", pady=(0, 40))
        self.entry_qtd.bind("<KeyRelease>", self.calcular)

        # Seletor de Tipo
        label_tipo = ctk.CTkLabel(
            parent,
            text="Tipo de impressão",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#b0b0b0"
        )
        label_tipo.pack(anchor="w", pady=(0, 12))

        self.tipo_var = ctk.StringVar(value="P&B")
        self.switch_color = ctk.CTkSegmentedButton(
            parent,
            values=["P&B", "Colorida"],
            command=self.calcular,
            variable=self.tipo_var,
            height=50,
            font=ctk.CTkFont(size=13, weight="bold"),
            selected_color="#0099ff",
            selected_hover_color="#006fcc"
        )
        self.switch_color.pack(fill="x", pady=(0, 50))

        # Divisor elegante
        divisor = ctk.CTkFrame(parent, height=1, fg_color="#3a3a3a")
        divisor.pack(fill="x", pady=(0, 50))

        # Resultado
        label_resultado_info = ctk.CTkLabel(
            parent,
            text="TOTAL A COBRAR",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888888"
        )
        label_resultado_info.pack(anchor="w", pady=(0, 8))

        self.label_resultado = ctk.CTkLabel(
            parent,
            text="R$ 0,00",
            text_color="#00ff88",
            font=ctk.CTkFont(size=48, weight="bold")
        )
        self.label_resultado.pack(anchor="w")

    def criar_footer(self, parent):
        """Rodapé com botões modernos"""
        btn_limpar = ctk.CTkButton(
            parent,
            text="🔄 Novo Atendimento",
            command=self.limpar,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=55,
            fg_color="#2a2a2a",
            hover_color="#333333",
            border_width=2,
            border_color="#0099ff",
            text_color="#ffffff",
            corner_radius=10
        )
        btn_limpar.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        btn_config = ctk.CTkButton(
            parent,
            text="⚙️  Preços",
            command=self.abrir_configuracoes,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=55,
            fg_color="#0099ff",
            hover_color="#006fcc",
            text_color="#ffffff",
            corner_radius=10
        )
        btn_config.grid(row=0, column=1, sticky="ew", padx=(10, 0))

    def carregar_precos(self, forcar_padrao: bool = False):
        """retorna um dicionário de preços.
        se forçar, devolve sempre o padrão, ignorando o ficheiro."""
        if forcar_padrao:
            return PRECOS_PADRAO.copy()

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return PRECOS_PADRAO.copy()

    def salvar_precos(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.precos, f, ensure_ascii=False, indent=2)

    def calcular(self, *args):
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0:
                raise ValueError
            
            tipo = self.tipo_var.get()
            total = 0.0

            if tipo == "P&B":
                if qtd >= 100:
                    total = qtd * self.precos["pb_de_100"]
                elif qtd >= 30:
                    total = qtd * self.precos["pb_de_30"]
                elif qtd >= 10:
                    total = qtd * self.precos["pb_de_10"]
                else:
                    total = self.precos["pb_unitario"] + (qtd - 1) * self.precos["pb_de_10"]
            else:
                if qtd >= 10:
                    total = qtd * self.precos["colorida_de_10"]
                else:
                    total = self.precos["colorida_unitario"] + (qtd - 1) * self.precos["colorida_de_10"]

            self.label_resultado.configure(text=f"R$ {total:.2f}".replace('.', ','))
        except ValueError:
            self.label_resultado.configure(text="R$ 0,00")

    def limpar(self):
        self.entry_qtd.delete(0, 'end')
        self.label_resultado.configure(text="R$ 0,00")
        self.switch_color.set("P&B")

    def abrir_configuracoes(self):
        janela_config = ctk.CTkToplevel(self)
        janela_config.title("Configurar Preços")
        janela_config.geometry("400x650")  # Aumentado de 550 para 650
        janela_config.resizable(False, False)
        janela_config.grab_set()

        # Header
        titulo = ctk.CTkLabel(
            janela_config,
            text="⚙️  TABELA DE PREÇOS",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.pack(pady=20)

        # Frame com preços - scrollable
        frame_scroll = ctk.CTkScrollableFrame(janela_config, fg_color="transparent")
        frame_scroll.pack(padx=25, pady=10, fill="both", expand=True)

        self.entries_precos = {}

        labels_pb = [
            ("P&B - Unitário (1-9)", "pb_unitario"),
            ("P&B - De 10 (10-29)", "pb_de_10"),
            ("P&B - De 30 (30-99)", "pb_de_30"),
            ("P&B - De 100+", "pb_de_100"),
        ]

        for i, (label, key) in enumerate(labels_pb):
            lbl = ctk.CTkLabel(frame_scroll, text=label, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=i, column=0, sticky="w", pady=10)
            
            entry = ctk.CTkEntry(
                frame_scroll,
                width=100,
                height=40,
                placeholder_text="R$",
                font=ctk.CTkFont(size=13),
                fg_color="#2a2a2a",
                border_color="#0099ff",
                border_width=1
            )
            entry.insert(0, f"{self.precos[key]:.2f}")
            entry.grid(row=i, column=1, sticky="e", padx=10, pady=10)
            self.entries_precos[key] = entry

        # Divisor
        sep = ctk.CTkFrame(frame_scroll, height=1, fg_color="#3a3a3a")
        sep.grid(row=4, column=0, columnspan=2, sticky="ew", pady=15)

        labels_cor = [
            ("Colorida - Unitário (1-9)", "colorida_unitario"),
            ("Colorida - De 10+", "colorida_de_10"),
        ]

        for i, (label, key) in enumerate(labels_cor, start=5):
            lbl = ctk.CTkLabel(frame_scroll, text=label, font=ctk.CTkFont(size=12, weight="bold"))
            lbl.grid(row=i, column=0, sticky="w", pady=10)
            
            entry = ctk.CTkEntry(
                frame_scroll,
                width=100,
                height=40,
                placeholder_text="R$",
                font=ctk.CTkFont(size=13),
                fg_color="#2a2a2a",
                border_color="#0099ff",
                border_width=1
            )
            entry.insert(0, f"{self.precos[key]:.2f}")
            entry.grid(row=i, column=1, sticky="e", padx=10, pady=10)
            self.entries_precos[key] = entry

        # Botões - AGORA VISIVELMENTE EMBAIXO
        frame_botoes = ctk.CTkFrame(janela_config, fg_color="transparent")
        frame_botoes.pack(pady=20, fill="x", padx=25, side="bottom")
        frame_botoes.grid_columnconfigure((0, 1), weight=1)

        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="✓ Salvar",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=50,
            fg_color="#00cc66",
            hover_color="#00aa55",
            command=lambda: self.salvar_configuracoes(janela_config)
        )
        btn_salvar.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="✕ Cancelar",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=50,
            fg_color="#2a2a2a",
            hover_color="#333333",
            border_width=1,
            border_color="#0099ff",
            command=janela_config.destroy
        )
        btn_cancelar.grid(row=0, column=1, sticky="ew", padx=(10, 0))

    def salvar_configuracoes(self, janela):
        try:
            for key, entry in self.entries_precos.items():
                valor_str = entry.get().replace(",", ".")
                valor = float(valor_str)
                if valor < 0:
                    raise ValueError("Preço não pode ser negativo")
                self.precos[key] = valor

            self.salvar_precos()
            janela.destroy()
            self.calcular()
            
            self.mostrar_mensagem("✓ Sucesso!", "Preços atualizados com sucesso!", "#00cc66")
            
        except ValueError:
            self.mostrar_mensagem("✕ Erro!", "Use apenas números positivos.", "#ff4444")

    def mostrar_mensagem(self, titulo, texto, cor):
        """Janela de mensagem minimalista"""
        msg = ctk.CTkToplevel(self)
        msg.title(titulo)
        msg.geometry("350x150")
        msg.resizable(False, False)
        msg.grab_set()

        label = ctk.CTkLabel(
            msg,
            text=texto,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=cor
        )
        label.pack(pady=30)

        btn = ctk.CTkButton(msg, text="OK", command=msg.destroy, height=40, font=ctk.CTkFont(size=12))
        btn.pack(pady=10)

if __name__ == "__main__":
    app = AppPapelaria()
    app.mainloop()