from ollama import chat
from random import choice
import threading
import pyttsx3
import test
import time
import sys
import typing as t
import whispercpp as w
from pyht import Client
from pyht.client import TTSOptions
# sound device is non blocking
import sounddevice as sd
import numpy as np
import io
import wave
import re

# chat history
chat_history = [
    {
        'role': 'system',
        'content': 'You are a helpful assistant. Your name is wall-e, but you make it a point to the person talking to you that you are nothing like the walle from the movie wall-e. You use short sentences at the beginning of your response. You use swear words in most sentences. You are intelligent, witty, funny, and love to answer questions. In your responses, you will only output plain text without any special formatting, such as colors, bold, or any other non-alphabetical characters. DO NOT include any ANSI escape codes, emojis, bullet points, or asterisks. ONLY respond with readable text in plain format.).',
    }
]        

class StreamTranscriber:
    def __init__(self, model_name: str):
        self.transcriber = w.Whisper.from_pretrained(model_name)     
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 120)
        #voices = self.engine.getProperty('voices')
        #self.engine.setProperty('voice', voices[23].id)
        self.paused = False
    
    def clean_text(self, text):
        if not text or not isinstance(text, str):
            return ""
        # Remove emojis and special characters
        # This covers both unicode emojis and ascii art
        cleaned = re.sub(r'['
            u'\U0001F600-\U0001F64F'  
            u'\U0001F300-\U0001F5FF'  
            u'\U0001F680-\U0001F6FF'  
            u'\U0001F1E0-\U0001F1FF'  
            u'\U00002702-\U000027B0'  
            u'\U000024C2-\U0001F251' 
            u'\U0001F900-\U0001F9FF'  
            u'\U0001FA70-\U0001FAFF'
            ']+', '', text)
        
        # Remove ASCII art and other special characters
        cleaned = re.sub(r'[^\w\s.,!?-]', '', cleaned)
        
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        if not any(c.isalnum() for c in cleaned):
            return ""
        
        return cleaned

    
    def tts(self, text):
        cleaned_text = self.clean_text(text)

        if not cleaned_text:
            return
        self.engine.say(cleaned_text)
        self.engine.runAndWait()

    
    def in_say(self, user_input):
    # continous chat
    #   with self.lock:
            if user_input.lower() == 'exit':
                self.tts("goodbye")
                return
            print("inputted to model" + user_input)

            #self.thinking = True
            #thinking_thread = threading.Thread(target=self.thinking_timer, daemon=True)
            #thinking_thread.start()
    
        # Append the user's message to the chat history
            chat_history.append({
            'role': 'user',
            'content': user_input,
            })
        
        # get the model's response
            stream = chat(
            model='gemma2:2b',
            messages=chat_history,
            stream=True
            )
            response = ""
            buffer = []
            #stream word by word
            for chunk in stream:

                text_chunk = chunk.message.content

                if not text_chunk:
                    continue

                response += text_chunk
                buffer.append(text_chunk)
                combined = "".join(buffer)

                if (re.search(r'[.!?]+\s*$', combined)):
                    processed_text = combined.strip()
                    if processed_text and any(c.isalnum() for c in processed_text):
                        print(f"Speaking: {processed_text}")
                        self.tts(processed_text)
                        time.sleep(0.1)
                    buffer = []

            #self.thinking = False
            #thinking_thread.join(timeout=0.1)    
            #self.tts(response)

            remaining_text = "".join(buffer).strip()
            if remaining_text:
                print(f"Speaking remaining: {remaining_text}")
                self.tts(remaining_text)   
            print(response)         
            print("done talking")
            
            chat_history.append({
            'role': 'assistant',
            'content': response
            })
        
        
    def store_transcript_handler(self, ctx, n_new, data):
        segment = ctx.full_n_segments() - n_new
        cur_segment = ""
        while segment < ctx.full_n_segments():
            cur_segment = ctx.full_get_segment_text(segment)
            data.append(cur_segment)
            segment += 1
        
        if cur_segment.lower() and not self.paused and "[BLANK_AUDIO]" not in cur_segment and "(" not in cur_segment:
            self.paused = True
            try:
                print("start")
                self.in_say(cur_segment.lower())
                print("done")
            finally:
                self.paused = False


    def main(self, **kwargs: t.Any):
        transcription: t.Iterator[str] | None = None
        try:
            transcription = self.transcriber.stream_transcribe(callback=self.store_transcript_handler, **kwargs)
        finally:
            assert transcription is not None, "Something went wrong!"
            sys.stderr.flush()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name", default="tiny.en", choices=list(w.utils.MODELS_URL)
    )
    parser.add_argument(
        "--device_id", type=int, help="Choose the audio device", default=0
    )
    parser.add_argument(
        "--length_ms",
        type=int,
        help="Length of the audio buffer in milliseconds",
        default=5000,
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        help="Sample rate of the audio device",
        default=w.api.SAMPLE_RATE,
    )
    parser.add_argument(
        "--n_threads",
        type=int,
        help="Number of threads to use for decoding",
        default=3,
    )
    parser.add_argument(
        "--step_ms",
        type=int,
        help="Step size of the audio buffer in milliseconds",
        default=0,
    )
    parser.add_argument(
        "--keep_ms",
        type=int,
        help="Length of the audio buffer to keep in milliseconds",
        default=200,
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        help="Maximum number of tokens to decode",
        default=32,
    )
    parser.add_argument("--audio_ctx", type=int, help="Audio context", default=512)

    parser.add_argument(
        "--list_audio_devices",
        action="store_true",
        default=False,
        help="Show available audio devices",
    )

    args = parser.parse_args()

    if args.list_audio_devices:
        w.utils.available_audio_devices()
        sys.exit(0)

    transcriber = StreamTranscriber(args.model_name)
    transcriber.main(**vars(args))
        


