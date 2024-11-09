import tkinter as tk
from datetime import datetime
import math

# Configurações iniciais da janela
janela = tk.Tk()
janela.title("Relógio Analógico")
janela.geometry("500x500")
janela.configure(bg="white")

# Criar um Canvas para desenhar o relógio
canvas = tk.Canvas(janela, width=500, height=500, bg="white")
canvas.pack()

# Função para desenhar o mostrador do relógio
def desenhar_mostrador():
    # Desenhar o círculo do mostrador
    canvas.create_oval(50, 50, 450, 450, outline="black", width=4)

    # Desenhar as marcações das horas
    for i in range(12):
        angulo = math.radians(i * 30)
        x1 = 250 + 180 * math.cos(angulo)
        y1 = 250 - 180 * math.sin(angulo)
        x2 = 250 + 200 * math.cos(angulo)
        y2 = 250 - 200 * math.sin(angulo)
        canvas.create_line(x1, y1, x2, y2, fill="black", width=3)

# Funções para desenhar os ponteiros
def desenhar_ponteiro_hora(horas, minutos):
    angulo = math.radians((horas % 12 + minutos / 60) * 30 - 90)
    x = 250 + 100 * math.cos(angulo)
    y = 250 + 100 * math.sin(angulo)
    return canvas.create_line(250, 250, x, y, fill="black", width=6, tags="ponteiro")

def desenhar_ponteiro_minuto(minutos, segundos):
    angulo = math.radians((minutos + segundos / 60) * 6 - 90)
    x = 250 + 140 * math.cos(angulo)
    y = 250 + 140 * math.sin(angulo)
    return canvas.create_line(250, 250, x, y, fill="blue", width=4, tags="ponteiro")

def desenhar_ponteiro_segundo(segundos):
    angulo = math.radians(segundos * 6 - 90)
    x = 250 + 180 * math.cos(angulo)
    y = 250 + 180 * math.sin(angulo)
    return canvas.create_line(250, 250, x, y, fill="red", width=2, tags="ponteiro")

# Função para atualizar os ponteiros
def atualizar_relogio():
    canvas.delete("ponteiro")  # Limpar os ponteiros antigos

    # Obter o horário atual
    agora = datetime.now()
    horas = agora.hour
    minutos = agora.minute
    segundos = agora.second

    # Desenhar os ponteiros atualizados
    desenhar_ponteiro_hora(horas, minutos)
    desenhar_ponteiro_minuto(minutos, segundos)
    desenhar_ponteiro_segundo(segundos)

    # Agendar a próxima atualização em 1000 ms (1 segundo)
    canvas.after(1000, atualizar_relogio)

# Função principal para iniciar o programa
def main():
    desenhar_mostrador()
    atualizar_relogio()
    janela.mainloop()

# Executa o programa principal
main()