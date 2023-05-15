# Import required libraries
import speech_recognition as sr
import os
import time
import openai
import boto3
from dotenv import load_dotenv
from playsound import playsound

load_dotenv()

# Configure OpenAI API key and model engine
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize AWS Polly client
polly_client = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION')
).client('polly')

# Initialize speech recognizer
r = sr.Recognizer()

print("Model = HaikuGPT")

# Define sound effect functions
def play_start_sound():
    playsound("start.mp3")

def play_stop_sound():
    playsound("start.mp3")

def play_thinking_sound():
    playsound("cpu.mp3")

# Loop forever
while True:
    # Play start sound and initialize audio source
    play_start_sound()
    with sr.Microphone() as source:
        print("Say something!")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # Listen for audio input until the user stops speaking
        audio = r.listen(source)
    # Play stop sound
    play_stop_sound()
    print("Got it, processing...")

    # Convert speech to text
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        
        print("Sending to OpenAI...")

            # Send message to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            max_tokens=100,
           messages=[{"role": "system", "content": "You are the best freestyle rapper in the world, and you're funny.  you stack rhymes inside of rhymes and find syllable patterns that ring in anyones ear"},
                     {"role": "user", "content": "what was your day like?"},
                     {"role": "assistant", "content": "My day was like a symphony, with highs and lows and in-between, From sunup to sundown, my rhymes were sharp and pristine,I battled all day, stacked rhymes within rhymes,Put my opponents to shame, left em dazed and blind, Every word a masterpiece, every verse a work of art,My day was a freestyle masterpiece, straight from the heart. I flowed like a river, my rhymes so cold theyre shivering,My freestyle game so strong, its like Im delivering The gospel of hip hop, spreading truth to the masses,My rhymes cut like a knife, leave the crowd gasping, My day was like a battle, a test of skill and wit,But I came out on top, cause my rhymes never quit."}, 
                     {"role": "user", "content": text}]
        )

        # Get response from OpenAI
        generated_text = response['choices'][0]['message']['content']
        print("Generated text:", generated_text)
        
        # Play thinking sound
        play_thinking_sound()


        # Read generated text aloud using AWS Polly
        response = polly_client.synthesize_speech(
            Text=generated_text,
            OutputFormat="mp3",
            VoiceId="Brian"
        )

        with open("output.mp3", "wb") as f:
            f.write(response['AudioStream'].read())

        playsound("output.mp3")
        #chill and let it sink in for a few seconds
        time.sleep(2)

    except sr.UnknownValueError:
        print("Oops! Didn't catch that.")
    except sr.RequestError as e:
        print("Uh oh! Couldn't do it; {0}".format(e))
