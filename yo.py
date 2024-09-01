import turtle
import math

# Configuración inicial
turtle.speed(0)  # Establece la velocidad de dibujo al máximo
turtle.bgcolor("sky blue")  # Establece el color de fondo

# Función para dibujar un pétalo
def draw_petal(t, radius, angle):
    t.circle(radius, angle)
    t.left(180 - angle)
    t.circle(radius, angle)
    t.left(180 - angle)

# Función para dibujar un girasol
def draw_sunflower():
    # Dibuja el tallo
    turtle.penup()
    turtle.goto(0, -250)
    turtle.pendown()
    turtle.color("green")
    turtle.right(90)
    turtle.forward(100)

    # Dibuja los pétalos del girasol
    turtle.penup()
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.color("orange")
    num_petals = 36  # Aumenta la cantidad de pétalos
    angle = 360 / num_petals
    radius = 150
    for _ in range(num_petals):
        draw_petal(turtle, radius, angle)
        turtle.left(angle)

    # Dibuja el centro del girasol
    turtle.penup()
    turtle.goto(0, 0)
    turtle.color("brown")
    turtle.dot(50)

# Dibujar el girasol
draw_sunflower()

# Oculta la tortuga y mantiene la ventana abierta
turtle.hideturtle()
turtle.done()
