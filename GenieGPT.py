from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_chat', methods=['POST'])
def start_chat():
    model_name = request.form['model']
    subprocess.Popen(['python3', f'{model_name}.py'])
    return f'Chat with {model_name} started!'

if __name__ == '__main__':
    app.run()

