import tkinter as tk
from datetime import datetime
import math
import asyncio

class RelogioAnalogico:
    def __init__(self, root, tamanho=400):
        """
        Inicializa o relógio analógico dentro de um widget Tkinter.

        Args:
            root (tk.Tk | tk.Frame): Janela ou frame principal onde o relógio será exibido.
            tamanho (int): Tamanho do mostrador do relógio em pixels. Padrão é 400.
        """
        self.root = root
        self.tamanho = tamanho
        self.raio = tamanho // 2 - 20  # Raio do mostrador para centralizar o relógio
        self.canvas = tk.Canvas(root, width=tamanho, height=tamanho, bg="white")
        self.canvas.pack()

        # Desenhar o mostrador uma única vez
        self.desenhar_mostrador()

    def desenhar_mostrador(self):
        """Desenha o mostrador do relógio, incluindo marcações para as horas."""
        # Desenhar o círculo do mostrador
        self.canvas.create_oval(10, 10, self.tamanho-10, self.tamanho-10, outline="black", width=4)

        # Desenhar as marcações das horas
        for i in range(12):
            angulo = math.radians(i * 30)
            x1 = self.tamanho / 2 + (self.raio - 20) * math.cos(angulo)
            y1 = self.tamanho / 2 - (self.raio - 20) * math.sin(angulo)
            x2 = self.tamanho / 2 + self.raio * math.cos(angulo)
            y2 = self.tamanho / 2 - self.raio * math.sin(angulo)
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    def desenhar_ponteiro(self, angulo, comprimento, cor, largura):
        """
        Desenha um ponteiro no mostrador.

        Args:
            angulo (float): Ângulo em radianos para o ponteiro.
            comprimento (float): Comprimento do ponteiro.
            cor (str): Cor do ponteiro.
            largura (int): Largura do ponteiro.
        """
        x = self.tamanho / 2 + comprimento * math.cos(angulo)
        y = self.tamanho / 2 - comprimento * math.sin(angulo)
        return self.canvas.create_line(
            self.tamanho / 2, self.tamanho / 2, x, y, fill=cor, width=largura, tags="ponteiro"
        )

    def atualizar_ponteiros(self):
        """Atualiza a posição dos ponteiros de hora, minuto e segundo com base no horário atual."""
        self.canvas.delete("ponteiro")  # Limpa os ponteiros antigos

        agora = datetime.now()
        hora = agora.hour % 12
        minuto = agora.minute
        segundo = agora.second

        # Ângulos dos ponteiros em radianos
        angulo_hora = math.radians((hora + minuto / 60) * 30 - 90)
        angulo_minuto = math.radians((minuto + segundo / 60) * 6 - 90)
        angulo_segundo = math.radians(segundo * 6 - 90)

        # Comprimentos dos ponteiros proporcionais ao tamanho do mostrador
        comprimento_hora = self.raio * 0.5
        comprimento_minuto = self.raio * 0.7
        comprimento_segundo = self.raio * 0.9

        # Desenha os ponteiros de hora, minuto e segundo
        self.desenhar_ponteiro(angulo_hora, comprimento_hora, "black", 6)
        self.desenhar_ponteiro(angulo_minuto, comprimento_minuto, "blue", 4)
        self.desenhar_ponteiro(angulo_segundo, comprimento_segundo, "red", 2)

    async def iniciar_relogio(self):
        """Inicia o relógio analógico com atualização dos ponteiros a cada segundo."""
        while True:
            self.atualizar_ponteiros()
            await asyncio.sleep(1)

'''
def iniciar_interface():
    """
    Inicializa a interface Tkinter e o loop assíncrono para o relógio analógico.
    """
    # Cria a janela principal
    root = tk.Tk()
    root.title("Relógio Analógico Responsivo")

    # Inicializa o relógio analógico
    relogio = RelogioAnalogico(root, tamanho=400)

    # Executa o relógio em modo assíncrono
    asyncio.run(relogio.iniciar_relogio())

    # Inicia o loop principal do Tkinter
    root.mainloop()

# Chamada da função principal para iniciar o relógio
iniciar_interface()
'''