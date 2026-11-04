import tkinter as tk
from tkinter import ttk, messagebox

class SistemaAcademicoLegado:
    def __init__(self, root):
        self.root = root
        self.root.title("Portal do Professor - Lançamento Legado")
        self.root.geometry("460x440")
        self.root.resizable(False, False)

        # Contador de lançamentos
        self.total_lancados = 0

        # Título da tela
        lbl_cabecalho = ttk.Label(
            root, 
            text="Sistema Acadêmico - Fechamento de Notas", 
            font=("Arial", 12, "bold")
        )
        lbl_cabecalho.pack(pady=10)

        # 1. Campo Matrícula / RA
        ttk.Label(root, text="Matrícula / RA:").pack(anchor="w", padx=40)
        self.ent_ra = ttk.Entry(root, width=40)
        self.ent_ra.pack(pady=3, padx=40)

        # 2. Campo Nome
        ttk.Label(root, text="Nome do Aluno:").pack(anchor="w", padx=40)
        self.ent_nome = ttk.Entry(root, width=40)
        self.ent_nome.pack(pady=3, padx=40)

        # 3. Campo Média Final
        ttk.Label(root, text="Média Final:").pack(anchor="w", padx=40)
        self.ent_media = ttk.Entry(root, width=40)
        self.ent_media.pack(pady=3, padx=40)

        # 4. Campo Situação
        ttk.Label(root, text="Situação (Aprovado / Reprovado):").pack(anchor="w", padx=40)
        self.ent_situacao = ttk.Entry(root, width=40)
        self.ent_situacao.pack(pady=3, padx=40)

        # Botão Salvar
        self.btn_salvar = ttk.Button(
            root, 
            text="Salvar Registro (Enter)", 
            command=self.salvar_registro
        )
        self.btn_salvar.pack(pady=15)

        # Rodapé com status do último registro gravado
        self.lbl_status = ttk.Label(
            root, 
            text="Aguardando início dos lançamentos...", 
            foreground="gray",
            font=("Arial", 9)
        )
        self.lbl_status.pack(pady=5)

        self.lbl_contador = ttk.Label(
            root, 
            text="Total lançados: 0", 
            font=("Arial", 9, "bold")
        )
        self.lbl_contador.pack(pady=2)

        # Vincula a tecla Enter ao salvamento quando estiver no botão ou formulário
        root.bind("<Return>", lambda event: self.salvar_registro())

        # Coloca o cursor direto no campo RA ao abrir
        self.ent_ra.focus_set()

    def salvar_registro(self):
        ra = self.ent_ra.get().strip()
        nome = self.ent_nome.get().strip()
        media = self.ent_media.get().strip()
        situacao = self.ent_situacao.get().strip()

        if not nome and not ra:
            return

        self.total_lancados += 1
        self.lbl_status.config(
            text=f"Gravado: {ra or 'SEM RA'} | {nome} | {media} ({situacao})",
            foreground="green"
        )
        self.lbl_contador.config(text=f"Total lançados: {self.total_lancados}")

        # Limpa os campos para a próxima digitação e volta o foco para o RA
        self.ent_ra.delete(0, tk.END)
        self.ent_nome.delete(0, tk.END)
        self.ent_media.delete(0, tk.END)
        self.ent_situacao.delete(0, tk.END)
        self.ent_ra.focus_set()

if __name__ == "__main__":
    app = tk.Tk()
    SistemaAcademicoLegado(app)
    app.mainloop()      