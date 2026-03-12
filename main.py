import customtkinter as ctk

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppPapelaria(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Orçamento - Papelaria")
        self.geometry("400x550")
        self.resizable(False, False)

        # Título Principal
        self.label_titulo = ctk.CTkLabel(self, text="Calculadora de Impressão", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.pack(pady=(20, 10))

        # Frame Central
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Input Quantidade
        self.label_qtd = ctk.CTkLabel(self.frame, text="Quantidade de Páginas:", font=ctk.CTkFont(size=14))
        self.label_qtd.pack(pady=(20, 0))
        
        self.entry_qtd = ctk.CTkEntry(self.frame, placeholder_text="Ex: 50", width=140, height=45, 
                                     font=ctk.CTkFont(size=20), justify="center")
        self.entry_qtd.pack(pady=10)
        self.entry_qtd.bind("<KeyRelease>", self.calcular)

        # Switch de Tipo (P&B ou Colorida)
        self.tipo_var = ctk.StringVar(value="pb")
        self.switch_color = ctk.CTkSegmentedButton(self.frame, values=["P&B", "Colorida"], 
                                                   command=self.calcular, variable=self.tipo_var)
        self.switch_color.pack(pady=20, padx=10)
        self.switch_color.set("P&B")

        # Divisor Visual
        self.linha = ctk.CTkFrame(self.frame, height=2, fg_color="gray")
        self.linha.pack(fill="x", padx=20, pady=10)

        # Área de Resultado
        self.label_info = ctk.CTkLabel(self.frame, text="Total a Cobrar:", font=ctk.CTkFont(size=14, slant="italic"))
        self.label_info.pack(pady=(10, 0))

        self.label_resultado = ctk.CTkLabel(self.frame, text="R$ 0,00", text_color="#27ae60", 
                                            font=ctk.CTkFont(size=38, weight="bold"))
        self.label_resultado.pack(pady=5)

        # Botão para Limpar
        self.btn_limpar = ctk.CTkButton(self, text="Novo Atendimento", fg_color="transparent", 
                                        border_width=2, text_color="white", command=self.limpar)
        self.btn_limpar.pack(pady=20)

    def calcular(self, *args):
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0: raise ValueError
            
            tipo = self.tipo_var.get()
            total = 0.0

            if tipo == "P&B":
                if qtd >= 100:
                    total = qtd * 0.25
                elif qtd >= 30:
                    total = qtd * 0.30
                elif qtd >= 10:
                    total = qtd * 0.50
                else:
                    total = 2.00 + (qtd - 1) * 0.50
            else: # Colorida
                if qtd >= 10:
                    total = qtd * 1.50
                else:
                    total = 2.00 + (qtd - 1) * 1.50

            self.label_resultado.configure(text=f"R$ {total:.2f}".replace('.', ','))
        except ValueError:
            self.label_resultado.configure(text="R$ 0,00")

    def limpar(self):
        self.entry_qtd.delete(0, 'end')
        self.label_resultado.configure(text="R$ 0,00")
        self.switch_color.set("P&B")

if __name__ == "__main__":
    app = AppPapelaria()
    app.mainloop()