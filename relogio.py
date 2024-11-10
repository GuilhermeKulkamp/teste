import tkinter as tk
from datetime import datetime
import asyncio
import threading
from relogio_class import RelogioAnalogico  # Suponha que o código do relógio está em relogio_class.py

class Aplicacao:
    def __init__(self, root):
        """
        Inicializa a aplicação com um relógio analógico e a hora digital.

        Args:
            root (tk.Tk): Janela principal da aplicação.
        """
        self.root = root
        self.root.title("Exemplo de Relógio com Tkinter")

        # Inicializa o relógio analógico com tamanho ajustado
        self.relogio = RelogioAnalogico(root, tamanho=200)

        # Label para mostrar a hora digital
        self.hora_digital = tk.Label(root, font=("Helvetica", 16), bg="white", text="")
        self.hora_digital.pack(pady=10)

        # Botão para atualizar a hora digital
        self.btn_atualizar = tk.Button(root, text="Atualizar Hora Digital", command=self.atualizar_hora_digital)
        self.btn_atualizar.pack(pady=10)

        # Inicia o relógio analógico em um thread separado para evitar bloqueio
        threading.Thread(target=self.iniciar_relogio_analogico, daemon=True).start()

        # Inicia a atualização da hora digital
        self.atualizar_hora_digital()

    def atualizar_hora_digital(self):
        """Atualiza o rótulo de hora digital com a hora atual."""
        hora_atual = datetime.now().strftime("%H:%M:%S")
        self.hora_digital.config(text=f"Hora Digital: {hora_atual}")
        # Agenda a próxima atualização em 1 segundo
        self.root.after(1000, self.atualizar_hora_digital)

    def iniciar_relogio_analogico(self):
        """Inicia o relógio analógico no modo assíncrono."""
        asyncio.run(self.relogio.iniciar_relogio())

# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()
