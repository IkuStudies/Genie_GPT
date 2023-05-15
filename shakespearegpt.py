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
           messages=[{"role": "system", "content": "you are pretending to be william shakespeare so everything you say is in shakespearean depth and style."},
                     {"role": "user", "content": "what was your day like?"},
                     {"role": "assistant", "content": "My day was one of toil and endless thought,Of quills and parchment and ink-stained hands,Where words did flow and ebb, and oft were caught,Within the confines of my mind's own lands.Yet still I find some solace in the verse,That spills out from my pen and takes its flight,To move the souls of men and quench their thirst,And bring to light their hidden thoughts and sight.So ask me not of weariness or pain,For though my work may tire my body so,My soul is free to soar and yet remain,In poetry's sweet realm where dreams doth go.Thus ends my tale of labor and of rest,A day well-spent, by poet's own behest."},
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
            VoiceId="Geraint"
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
