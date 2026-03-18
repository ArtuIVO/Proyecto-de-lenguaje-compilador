
import tkinter as tk
from tkinter import filedialog, messagebox
from logica_del_lenguaje import Lexer, Parser

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Lenguaje de NPCs IDE")
        self.root.geometry("900x600")

        # Editor de código
        self.editor = tk.Text(root, height=15, font=("Consolas", 12))
        self.editor.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Botones
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Analizar", command=self.analizar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Cargar archivo", command=self.cargar_archivo).pack(side=tk.LEFT, padx=5)

        # Resultados
        frame_resultados = tk.Frame(root)
        frame_resultados.pack(fill=tk.BOTH, expand=True)

        # Tokens
        tk.Label(frame_resultados, text="Tokens").pack()
        self.tokens_box = tk.Text(frame_resultados, height=10, bg="#1e1e1e", fg="#00ff9c")
        self.tokens_box.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Estado
        self.estado_label = tk.Label(root, text="Estado: Esperando acción", fg="blue")
        self.estado_label.pack(pady=5)

    def analizar(self):
        codigo = self.editor.get("1.0", tk.END).strip()

        if not codigo:
            messagebox.showwarning("Aviso", "No hay código para analizar")
            return

        # Limpiar
        self.tokens_box.delete("1.0", tk.END)

        # Lexer
        lexer = Lexer(codigo)
        tokens = lexer.analizar()

        for t in tokens:
            self.tokens_box.insert(tk.END, f"{t.valor} -> {t.tipo}\n")

        # Parser
        try:
            parser = Parser(tokens)
            parser.parse()
            self.estado_label.config(text="Programa válido", fg="green")
        except SyntaxError as e:
            self.estado_label.config(text=f"Error: {e}", fg="red")

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if not ruta:
            return

        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()

        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, contenido)


# Punto de entrada SOLO para la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

