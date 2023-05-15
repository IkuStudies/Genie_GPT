#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import speech_recognition as sr
import os
import time
import openai
import boto3
from dotenv import load_dotenv
from playsound import playsound
import tempfile

load_dotenv()

# Configure OpenAI API key and model engine
openai.api_key = os.environ.get('OPENAI_API_KEY')
model_engine = os.environ.get('MODEL_ENGINE')

# Initialize speech recognizer
r = sr.Recognizer()

# Initialize AWS Polly client
polly = boto3.client('polly',
                     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                     aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                     region_name=os.environ.get('AWS_REGION'))

print("Model engine:", model_engine)

# Define function to play sound effect
def play_sound_effect(sound_file):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(sound_file.read())
        f.flush()
        f.seek(0)
        playsound(f.name)

# Loop forever
while True:
    # Play sound effect to indicate start of listening
    start_sound = open('start.mp3', 'rb')
    play_sound_effect(start_sound)
    
    # Initialize audio source
    with sr.Microphone() as source:
        print("Say something!")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # Listen for audio input until the user stops speaking
        audio = r.listen(source)
        print("Got it, processing...")  

    # Play sound effect to indicate end of listening
    end_sound = open('start.mp3', 'rb')
    play_sound_effect(end_sound)    
    # Convert speech to text
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        print("Sending to OpenAI...")
        

        # Send message to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": text
                },
                
            ]
        )

        processing = open('cpu.mp3', 'rb')
        play_sound_effect(processing)
       # Get response from OpenAI
        generated_text = response['choices'][0]['message']['content']
        print("Generated text:", generated_text)
        

        # Read generated text aloud using AWS Polly
        response = polly.synthesize_speech(Text=generated_text,
                                           OutputFormat='mp3',
                                           VoiceId='Geraint')
        play_sound_effect(response['AudioStream'])

    except sr.UnknownValueError:
        print("Oops! Didn't catch that.")
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except Exception as e:
        print("Error:", e)


# In[ ]:




