Read Me

contents of the project are jupyter notebooks with various attempts and drafts that led to the .py files used in the program.  once you follow these steps go to the Genie-GPT directory and run "python GenieGPT.py" in the terminal and it should give you an ip to open and select your chat model and press start.  i need to update the microphone coming on and off sound, they are the same sound, but just start talking and it should pick it up.  it takes a bit of time and could be smoother but this is V1, any ideas lmk i would like to improve the program  


this is the documentation I used to make this app
https://platform.openai.com/docs/api-reference
https://platform.openai.com/docs/models

API call-response structure is important to study in understanding how the API works.  this was just an easy app, the next thing I'm going to work on is training the models on data, and giving them a long term memory and really figuring out how to tease out super relevant chatbots who know exactly what to recommend.

installation
download the repository, go to that directory and run pip install requirements.txt

go to hidden.env_template, put in your API's and save as .env

input your AWS key and secret key (both require credit card but are free to set up.)

review the rate of use in the documentation(this app will be very cheap to use, uses few tokens, but review rates in API's just to be sure)

if you'd like to mess with the configuration and experiment with it go right ahead.  there's more configurable settings you can add to the code, just need to look at documentation above


there are a few .py files.  each is named for the personality the program is built to emulate.
go to the .py files to review the structure of the API call.  don't change the format but
you can configure and customize any chatbot by giving it a background under the hood.

I'm still figuring out how to use the json files to give it contextual memory and longterm memory, which i will update once i wrap my mind around that.

just don't change the format for the API call and response structure or you will get looney responses from left field.
you can also configure the voice being used.  the options for voices can be seen by running this code in a jupyter notebook with your region name, and you can probably further configure the voices further but I haven't been able to find those details, but run this and it will print available voices

        import boto3

        client = boto3.client('polly', region_name='us-west-2')

        voices = client.describe_voices()
        print(voices)


if you fork and use this code, please thank @ikustudies and direct to github.com/ikustudies
and if you'd like to buy me a coffee or hire me for anything I can hack into whatever, or if you'd like to support my research
email me ikustudies@gmail.com let's talk

I'm digital nomad living near the amazon jungle, always looking for more experience and also very much looking for remote work, i will take anything, and i'm cheap

thanks
Josh T 
Ikustudies
