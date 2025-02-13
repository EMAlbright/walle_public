# Smart Robot with AI Integration
![IMG_1375](https://github.com/user-attachments/assets/c3badb07-4a3e-4212-9fd9-acf7228042f0)
![IMG_1376](https://github.com/user-attachments/assets/c98e4c54-a2db-4296-9c06-018852cc4667)

This project is a custom-built smart robot designed to follow people and converse with them using AI. The robot features movement control via TT motors, person tracking using a PI AI camera, and speech synthesis with Gemma 2b LLM. It combines computer vision, speech processing, and AI to interact with users in a dynamic way.

## Features

- **Person Tracking**: The robot uses a PI AI camera to detect and track people.
- **Speech Interaction**: The robot communicates with users using speech synthesis powered by Gemma 2b LLM.
- **Movement Control**: The robot can move using four TT motors, controlled via GPIO pins.
- **AI Camera Integration**: The robot employs an AI camera for real-time object detection and tracking.

## Project Breakdown

### 1. **`llm.py`**
This file manages interaction with the OpenAI API for image analysis. The robot captures images using the PI AI camera and sends them to the OpenAI API for processing. The `llm.py` script encodes the captured image into base64 format and then sends it to the API for description and analysis. 

- **encodeImage()**: Reads an image file, encodes it into base64 format for API transmission.
- **analyze()**: Sends the encoded image to the OpenAI API and retrieves a descriptive response.

### 2. **`person_follow.py`**
This file enables the robot to track and follow people. It integrates with the PI AI camera to detect persons in the environment. The robot moves towards the detected person based on distance and direction calculated from the camera’s field of view.

- **auto_move()**: Decides the robot's movement based on the person's position (left, right, forward, or stop).
- **forward()**, **backward()**, **left()**, **right()**: Control the robot’s motors to move in the desired direction.
- **stop()**: Stops all motor movement.

### 3. **`gemma.py`**
The `gemma.py` file handles speech synthesis and voice interaction. The Gemma 2b LLM is used for speech generation based on user input. This allows the robot to have dynamic conversations. The file also implements an audio transcription feature using WhisperCPP, converting speech to text for processing.

**Code Explanation:**
- **StreamTranscriber**: Handles audio transcription and text-to-speech (TTS). It listens to spoken input, transcribes it, and generates a response using Gemma 2b.
- **in_say()**: Takes user input, sends it to Gemma for processing, and reads aloud the response.

### 4. **`test_motors.py`**
This is a test file used to manually control the robot's motors using keyboard inputs. It allows you to test forward, backward, left, and right movement of the robot in a simple manner without relying on any camera input.

- **forward()**, **backward()**, **left()**, **right()**: Correspond to manual movement controls for testing purposes.
- **keyboard.is_pressed()**: Listens for specific keyboard keys (W, A, S, D) to control robot movement.

The script lets you control the robot using keyboard keys, simulating how it would move based on real-time inputs.

### How it Works
1. **Tracking**: The robot constantly scans for people in its field of vision using the PI AI camera. Once a person is detected, the robot calculates its position relative to the center of the camera and moves accordingly to stay in pursuit of the person.
   
2. **Speech Interaction**: The robot interacts with users via speech synthesis (Gemma 2b LLM). It can respond to questions or make simple conversational remarks based on the user's input.

3. **Movement Control**: The robot uses TT motors to move in four directions (forward, backward, left, and right). Motor control is handled via GPIO pins on a Raspberry Pi.

4. **AI Integration**: The robot integrates a custom AI system (Gemma 2b LLM and OpenAI) for image analysis and speech interaction. The camera detects the person and sends data to the LLM, which generates a response.

## Work in Progress

This project is still a work in progress. While the core features such as person tracking, speech interaction, and movement control have been implemented, there are still areas that require further refinement and development. Currently, the robot is in a prototype stage, and future updates will focus on improving the accuracy of person tracking, enhancing the conversational AI capabilities, and optimizing motor control for smoother movement.

### Hardware Requirements
- Raspberry Pi (with GPIO pins enabled)
- PI AI camera (IMX500) for vision
- Four TT motors for movement
- Gemma 2b LLM for speech synthesis
- Microphone and speaker for audio input/output

### Software Requirements
- Python 3.x
- Required Python libraries: `openai`, `gpiozero`, `pyttsx3`, `pyht`, `whispercpp`, `sounddevice`, `ollama`
- OpenAI API key for image analysis (optional for external analysis)
- Local AI models for speech synthesis and transcription
