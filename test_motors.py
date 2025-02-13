from gpiozero import Motor
from time import sleep
import keyboard

motorA = Motor(forward=17, backward=27)
motorB = Motor(forward=22, backward=23)

def stop():
    motorA.stop()
    motorB.stop()

def forward(speed):
    motorA.forward(speed)
    motorB.forward(speed)

def backward(speed):
    motorA.backward(speed)
    motorB.backward(speed)
    
def right(speed):
    motorA.backward(speed)
    motorB.forward(speed)

def left(speed):
    motorB.backward(speed)
    motorA.forward(speed)

current_action = None

while True:
    if keyboard.is_pressed('w') and current_action != 'forward':
        forward(1)
        current_action = 'forward'
    elif keyboard.is_pressed('s') and current_action != 'backward':
        backward(1)
        current_action = 'backward'
    elif keyboard.is_pressed('a') and current_action != 'left':
        left(1)
        current_action = 'left'
    elif keyboard.is_pressed('d') and current_action != 'right':
        right(1)
        current_action = 'right'
    elif not (keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('a') or keyboard.is_pressed('d')):
        if current_action is not None:
            stop()
            current_action = None

    sleep(0.1)



