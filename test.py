import threading
import person_follow
import gemma

if __name__ == "__main__":
    scribe = gemma.StreamTranscriber("tiny.en")
    speechThread = threading.Thread(target=scribe.main, daemon=True)
    moveThread = threading.Thread(target=person_follow.robot_start, daemon=True)
    
    speechThread.start()
    moveThread.start()
    speechThread.join()
    moveThread.join()
