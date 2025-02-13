from ai_camera import IMX500Detector
import time

from gpiozero import Motor
from time import sleep

from llm import encodeImage, analyze

#motorA = Motor(forward=17, backward=27)
#motorB = Motor(forward=22, backward=23)
    
camera = IMX500Detector()

# Start the detector with preview window
camera.start(show_preview=True)

# needing to detect distance from object ahead?
# distance = object size * focal length / b box size (pixels)
#  for now, it will just follow people around
# focal length = 14.05 mm
# assume height of person is 5 foot 10

# Main loop
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
        if label == "person" and confidence > 0.4:
            temp_path = "/home/ealb/Desktop/walle/temp_file.jpeg"
            # note: this is constatntly re capturing but thats just because person is in frame
            # with command it will only do it once
            camera.capture_frame(temp_path)
            
            # encode to base 64
            encoded_img = encodeImage("/home/ealb/Desktop/walle/temp_file.jpeg")
            vision_response = analyze(encoded_img)
            print(vision_response)
            break  
    
    # Small delay to prevent overwhelming the system
    time.sleep(0.1)
