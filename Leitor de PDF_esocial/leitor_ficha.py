#!/usr/bin/env python3
"""
Leitor de Fichas de Registro com IA (Gemini)
Suporta PDFs digitais e scaneados - gratuito via Google AI Studio
"""

import sys
import os
import json
import base64
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

try:
    from pypdf import PdfReader
    from google import genai
except ImportError as e:
    print(f"Dependência faltando: {e}")
    print("Rode: pip install pypdf google-genai")
    sys.exit(1)


CAMPOS = [
    "NOME",
    "DATA_NASCIMENTO",
    "CPF",
    "CTPS",
    "SERIE",
    "UF",
    "SEXO",
    "NUMERO_ESOCIAL",
    "DATA_ADMISSAO",
    "CARGO",
]

PROMPT = """Você é especialista em leitura de fichas de registro de empregados brasileiros (CLT).
Esta é uma imagem de uma ficha de registro. Leia VISUALMENTE todo o documento e extraia os campos abaixo.

MAPEAMENTO DOS CAMPOS NA FICHA:
- NOME: campo "Empregado" no topo da ficha (nome completo do funcionário)
- DATA_NASCIMENTO: campo "Data do nascimento" (formato DD/MM/AAAA)
- CPF: campo "CPF" (formato XXX.XXX.XXX-XX)
- CTPS: campo "CTPS" — pegue apenas o número principal (ex: 46294072), não a série
- SERIE: campo "Série" ou "Série CTPS" — número logo após o número da CTPS (ex: 2867)
- UF: campo "UF CTPS" — estado de emissão da carteira de trabalho (2 letras, ex: SP)
- SEXO: campo "Sexo" (Masculino ou Feminino)
- NUMERO_ESOCIAL: campo "Matrícula eSocial" ou "NIT" ou "PIS/PASEP" — qualquer um destes
- DATA_ADMISSAO: campo "Data de Admissão" (formato DD/MM/AAAA)
- CARGO: campo "Cargo" ou "Função" — descrição do cargo do funcionário

REGRAS:
- Se um campo não existir ou estiver ilegível, use null
- Formate datas como DD/MM/AAAA
- CPF como XXX.XXX.XXX-XX
- Retorne SOMENTE o JSON abaixo, sem markdown, sem explicação

{
  "NOME": "...",
  "DATA_NASCIMENTO": "...",
  "CPF": "...",
  "CTPS": "...",
  "SERIE": "...",
  "UF": "...",
  "SEXO": "...",
  "NUMERO_ESOCIAL": "...",
  "DATA_ADMISSAO": "...",
  "CARGO": "..."
}"""


def extrair_texto_pdf(caminho: str) -> str:
    reader = PdfReader(caminho)
    texto = ""
    for pagina in reader.pages:
        texto += pagina.extract_text() or ""
    return texto.strip()


def extrair_com_ia(caminho: str, api_key: str) -> dict:
    client = genai.Client(api_key=api_key)

    ext = os.path.splitext(caminho)[1].lower()
    with open(caminho, "rb") as f:
        arquivo_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    if ext == ".pdf":
        arquivo_part = {"type": "document", "data": arquivo_b64, "mime_type": "application/pdf"}
    elif ext in (".jpg", ".jpeg"):
        arquivo_part = {"type": "image", "data": arquivo_b64, "mime_type": "image/jpeg"}
    elif ext == ".png":
        arquivo_part = {"type": "image", "data": arquivo_b64, "mime_type": "image/png"}
    else:
        raise ValueError(f"Formato não suportado: {ext}\nUse PDF, JPG ou PNG.")

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=[
            arquivo_part,
            {"type": "text", "text": PROMPT},
        ],
    )

    conteudo = interaction.output_text.strip()
    conteudo = conteudo.replace("```json", "").replace("```", "").strip()
    return json.loads(conteudo)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Leitor de Ficha de Registro")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self._api_key = os.environ.get("GEMINI_API_KEY", "")
        self._pdf_path = None
        self._build_ui()
        self._centralizar()

    def _centralizar(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        BG     = "#1e1e2e"
        CARD   = "#2a2a3e"
        ACCENT = "#7c6af7"
        TEXT   = "#cdd6f4"
        MUTED  = "#6c7086"

        # Header
        hdr = tk.Frame(self, bg=BG, padx=20, pady=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📋 Leitor de Ficha de Registro",
                 font=("Segoe UI", 16, "bold"), fg=TEXT, bg=BG).pack(anchor="w")
        tk.Label(hdr, text="Powered by Google Gemini  •  Suporta PDFs digitais e scaneados",
                 font=("Segoe UI", 9), fg=MUTED, bg=BG).pack(anchor="w")

        # API Key
        if not self._api_key:
            kf = tk.Frame(self, bg=CARD, padx=20, pady=12)
            kf.pack(fill="x", padx=20)
            tk.Label(kf, text="API Key do Google AI Studio:", font=("Segoe UI", 10),
                     fg=TEXT, bg=CARD).pack(anchor="w")
            self._key_var = tk.StringVar()
            tk.Entry(kf, textvariable=self._key_var, show="•",
                     font=("Segoe UI", 10), bg="#313244", fg=TEXT,
                     insertbackground=TEXT, relief="flat", width=52).pack(fill="x", pady=(4, 0))
            self._key_var.trace_add("write", lambda *_: setattr(self, "_api_key", self._key_var.get()))

        tk.Frame(self, bg=MUTED, height=1).pack(fill="x", padx=20, pady=20)

        # Área de seleção
        drop = tk.Frame(self, bg=CARD, padx=20, pady=18, cursor="hand2")
        drop.pack(fill="x", padx=20)
        self._file_label = tk.Label(drop, text="📂  Clique para selecionar o PDF",
                                    font=("Segoe UI", 11), fg=ACCENT, bg=CARD)
        self._file_label.pack()
        self._path_label = tk.Label(drop, text="", font=("Segoe UI", 9), fg=MUTED, bg=CARD)
        self._path_label.pack()
        for w in (drop, self._file_label):
            w.bind("<Button-1>", self._selecionar)

        # Botão
        self._btn = tk.Button(
            self, text="✨  Extrair com IA",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg="white", activebackground="#6a5ae0",
            relief="flat", padx=20, pady=10, cursor="hand2",
            command=self._iniciar, state="disabled"
        )
        self._btn.pack(pady=20)

        self._status = tk.Label(self, text="", font=("Segoe UI", 10), fg=MUTED, bg=BG)
        self._status.pack()

        # Tabela
        tf = tk.Frame(self, bg=BG, padx=20, pady=20)
        tf.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("C.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=("Segoe UI", 10))
        style.configure("C.Treeview.Heading", background="#313244", foreground=TEXT,
                        font=("Segoe UI", 10, "bold"))
        style.map("C.Treeview", background=[("selected", ACCENT)])

        self._tree = ttk.Treeview(tf, columns=("campo", "valor"),
                                  show="headings", height=len(CAMPOS), style="C.Treeview")
        self._tree.heading("campo", text="Campo")
        self._tree.heading("valor", text="Valor extraído  (clique duplo para copiar)")
        self._tree.column("campo", width=180, anchor="w")
        self._tree.column("valor", width=400, anchor="w")
        self._tree.pack(fill="both", expand=True)
        self._tree.bind("<Double-1>", self._copiar_linha)

        # Botão copiar tudo
        self._btn_copiar = tk.Button(
            tf, text="📋  Copiar tudo",
            font=("Segoe UI", 10), bg="#313244", fg=TEXT,
            activebackground="#414155", relief="flat",
            padx=14, pady=6, cursor="hand2",
            command=self._copiar_tudo, state="disabled"
        )
        self._btn_copiar.pack(anchor="e", pady=(8, 0))

    def _copiar_linha(self, event):
        item = self._tree.identify_row(event.y)
        if not item:
            return
        campo, valor = self._tree.item(item, "values")
        if valor and valor != "—":
            self.clipboard_clear()
            self.clipboard_append(valor)
            self._status.config(text=f"📋  {campo} copiado!")
            self.after(2000, lambda: self._status.config(text="✅  Extração concluída!"))

    def _copiar_tudo(self):
        linhas = []
        for item in self._tree.get_children():
            campo, valor = self._tree.item(item, "values")
            linhas.append(f"{campo}: {valor}")
        texto = "\n".join(linhas)
        self.clipboard_clear()
        self.clipboard_append(texto)
        self._status.config(text="📋  Todos os campos copiados!")
        self.after(2000, lambda: self._status.config(text="✅  Extração concluída!"))

    def _selecionar(self, *_):
        path = filedialog.askopenfilename(
            title="Selecionar Ficha de Registro",
            filetypes=[
                ("Todos suportados", "*.pdf *.jpg *.jpeg *.png"),
                ("PDF", "*.pdf"),
                ("Imagem", "*.jpg *.jpeg *.png"),
            ]
        )
        if path:
            self._pdf_path = path
            self._file_label.config(text=f"📄  {os.path.basename(path)}")
            self._path_label.config(text=path)
            self._btn.config(state="normal")
            self._status.config(text="")
            for r in self._tree.get_children():
                self._tree.delete(r)
            self._btn_copiar.config(state="disabled")

    def _iniciar(self):
        if not self._api_key:
            messagebox.showwarning("API Key", "Informe a API Key do Google AI Studio.")
            return
        self._btn.config(state="disabled", text="⏳  Processando...")
        self._status.config(text="Enviando para o Gemini...")
        for r in self._tree.get_children():
            self._tree.delete(r)
        threading.Thread(target=self._extrair, daemon=True).start()

    def _extrair(self):
        try:
            dados = extrair_com_ia(self._pdf_path, self._api_key)
            self.after(0, self._mostrar, dados)
        except json.JSONDecodeError:
            self.after(0, self._erro, "A IA retornou formato inesperado. Tente novamente.")
        except Exception as e:
            self.after(0, self._erro, str(e))

    def _mostrar(self, dados: dict):
        for campo in CAMPOS:
            self._tree.insert("", "end", values=(campo, dados.get(campo) or "—"))
        self._status.config(text="✅  Extração concluída!")
        self._btn.config(state="normal", text="✨  Extrair com IA")
        self._btn_copiar.config(state="normal")

    def _erro(self, msg: str):
        self._status.config(text="❌  Erro")
        self._btn.config(state="normal", text="✨  Extrair com IA")
        messagebox.showerror("Erro", msg)


if __name__ == "__main__":
    App().mainloop()