from ai_camera import IMX500Detector
import time
from time import sleep
from gpiozero import Motor
import numpy as np
motorA = Motor(forward=17, backward=27)
motorB = Motor(forward=22, backward=23)
CAM_CENTER_X = 1014
CAM_CENTER_Y = 760

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
    motorA.stop()
    motorB.forward(speed)

def left(speed):
    motorB.stop()
    motorA.forward(speed)

# take in x and y position to know how to rotate
# take in distance to know how to move (forward and back)
def auto_move(x, y, distance):
    # person on the right, turn right
    if x > CAM_CENTER_X + 50.0:
        right(.25)
    
    # person on the left, turn left
    elif x < CAM_CENTER_X - 50.0:
        left(.25)
    else:
        stop()
        
    # too close
    if distance < 1.0:
        stop()
    
    # person small distance
    elif distance > 1 and distance < 1.25:
        forward(1.0)
    
    # person medium distance
    elif distance > 1.5 and distance < 2.0:
        forward(1.0)
    
    # person large distance
    elif distance >= 2.0:
        forward(1.0)
    

# distance = object size * focal length / b box size (pixels)
# focal length = 14.05 mm
# assume height of person is 5 foot 10
# camera res 2028x1520

def robot_start():
    camera = IMX500Detector()

    # Start the detector with preview window
    camera.start(show_preview=True)
    while True:
        # Get the latest detections
        detections = camera.get_detections()
        # Get the labels for reference
        labels = camera.get_labels()
        # Process each detection
        for detection in detections:
            label = labels[int(detection.category)]
            confidence = detection.conf
            # Example: Print when a person is detected with high confidence
            if label == "person" and confidence > 0.5:
                # 60 inches = 1.778 m
                # 14.05 mm focal length
                x, y, w, h = detection.box
                personCenterX = (x + w) // 2
                personCenterY = (y + h) // 2
                if w > 0:
                    distance = (1778  * 14.05) / w
                print(distance/100)
                auto_move(personCenterX, personCenterY, distance/100)
                break  
    
        # Small delay to prevent overwhelming the system
        time.sleep(0.1)
