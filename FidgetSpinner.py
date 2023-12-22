from turtle import *

# Initial state dictionary with a 'turn' key
state = {'turn': 0}

# Function to draw the spinner
def spinner():
    clear()
    angle = state['turn'] / 15
    right(angle)
    forward(100)
    dot(120, 'red')
    back(100)
    right(120)
    forward(100)
    dot(120, 'green')
    back(100)
    right(120)
    forward(100)
    dot(120, 'blue')
    back(100)
    right(120)
    update()

# Function to animate the spinner
def animate():
    if state['turn'] > 0:
        state['turn'] -= 1

    spinner()
    ontimer(animate, 20)

# Function to increase the spinner's speed
def flick():
    state['turn'] += 10

# Set up the Turtle screen
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
width(20)

# Bind the 'space' key to the flick function
onkey(flick, 'space')
listen()

# Start the animation
animate()

# Finish the Turtle graphics program
done()
