from transformers import pipeline
from flask import Flask, render_template, request , redirect, url_for

import secrets

secret_key = secrets.token_hex(16)


app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/generate', methods=['POST'])
def generate():
    raw_text = request.form['input_text1']
    raw_text = request.form['input_text2']
    new_text = raw_text + "project"

    generator = pipeline('text-generation', model='gpt2')
    output = generator(new_text, min_length=200,max_length=300, num_return_sequences=1)

    generated_text = output[0]['generated_text']
    generated_text = generated_text.split(new_text, 1)[-1].strip()

    # Redirect the user to the result page
    return redirect(url_for('result', new_text=new_text, generated_text=generated_text))



@app.route('/result')
def result():
    new_text = request.args.get('new_text')
    generated_text = request.args.get('generated_text')
    
    return render_template('result.html', new_text=new_text, generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
