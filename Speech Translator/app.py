from flask import Flask, request, jsonify, render_template
from googletrans import Translator
from gtts import gTTS
import os
import time

app = Flask(__name__)
translator = Translator()

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text')
        dest_lang = data.get('dest_lang')
        
        # Translate Text
        translation = translator.translate(text, dest=dest_lang)
        
        # Generate Speech - Wrap in try/except because gTTS doesn't support ALL languages
        filename = None
        try:
            tts = gTTS(translation.text, lang=dest_lang)
            filename = f"speech_{int(time.time())}.mp3"
            filepath = os.path.join('static', filename)
            tts.save(filepath)
        except Exception as e:
            print(f"Audio not supported for this language: {e}")

        return jsonify({
            'translated_text': translation.text,
            'audio_url': f"/static/{filename}" if filename else None
        })
    except Exception as e:
        print(f"Translation Error: {e}")
        return jsonify({'error': "Translation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)