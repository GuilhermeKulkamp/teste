import turtle
import time
from datetime import datetime

# Configuração da tela
tela = turtle.Screen()
tela.title("Relógio Analógico")
tela.setup(width=600, height=600)
tela.tracer(0)  # Desativa a atualização automática da tela para mais eficiência

# Tartaruga para desenhar o mostrador
mostrador = turtle.Turtle()
mostrador.hideturtle()
mostrador.speed(0)

# Tartarugas para os ponteiros de hora, minuto e segundo
ponteiro_hora = turtle.Turtle()
ponteiro_hora.shape("arrow")
ponteiro_hora.color("black")
ponteiro_hora.shapesize(stretch_wid=0.4, stretch_len=8)
ponteiro_hora.speed(0)

ponteiro_minuto = turtle.Turtle()
ponteiro_minuto.shape("arrow")
ponteiro_minuto.color("blue")
ponteiro_minuto.shapesize(stretch_wid=0.3, stretch_len=10)
ponteiro_minuto.speed(0)

ponteiro_segundo = turtle.Turtle()
ponteiro_segundo.shape("arrow")
ponteiro_segundo.color("red")
ponteiro_segundo.shapesize(stretch_wid=0.2, stretch_len=12)
ponteiro_segundo.speed(0)

# Função para desenhar o mostrador do relógio
def desenhar_mostrador():
    mostrador.penup()
    mostrador.goto(0, -250)
    mostrador.pendown()
    mostrador.circle(250)
    mostrador.penup()
    mostrador.goto(0, 0)
    
    # Desenhar as marcações das horas
    for angulo in range(0, 360, 30):
        mostrador.penup()
        mostrador.setheading(angulo)
        mostrador.forward(220)
        mostrador.pendown()
        mostrador.forward(30)
        mostrador.penup()
        mostrador.goto(0, 0)

# Função para atualizar a posição dos ponteiros
def atualizar_relogio():
    agora = datetime.now()
    hora = agora.hour % 12
    minuto = agora.minute
    segundo = agora.second
    
    # Atualiza os ângulos dos ponteiros
    angulo_hora = (hora + minuto / 60) * 30  # Cada hora são 30 graus
    angulo_minuto = (minuto + segundo / 60) * 6  # Cada minuto são 6 graus
    angulo_segundo = segundo * 6  # Cada segundo são 6 graus
    
    # Define as posições dos ponteiros
    ponteiro_hora.setheading(90 - angulo_hora)
    ponteiro_minuto.setheading(90 - angulo_minuto)
    ponteiro_segundo.setheading(90 - angulo_segundo)
    
    # Atualiza a tela e agenda a próxima atualização
    tela.update()
    tela.ontimer(atualizar_relogio, 1000)

# Função principal
def main():
    desenhar_mostrador()
    atualizar_relogio()
    tela.mainloop()

# Executa o programa principal
main()
