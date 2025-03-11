import flask
import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.config["Upload_Folder"] = "/home/muhammed-shafeeh/AI_ML/GenAI/audio_translation/static"

# Ensure the upload folder exists
if not os.path.exists(app.config["Upload_Folder"]):
    os.makedirs(app.config["Upload_Folder"])

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        language = request.form["language"]
        files = request.files["files"]

        if files:
            filename = files.filename
            file_path = os.path.join(app.config["Upload_Folder"], filename)
            files.save(file_path)
            
            print(f"File saved at: {file_path}")  # Debugging to check if file is saved
            
            # Open the uploaded audio file
            with open(file_path, "rb") as audio_file:
                # Initialize OpenAI client
                client = openai.OpenAI()

                # Transcribe the audio
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You will be provided with a sentence in english, and your task is to translate it into {language}"
                    },
                    {
                        "role": "user",
                        "content": transcript.text
                    }
                ],
                max_tokens=256,
                temperature=0
            )
            translated_text = response.choices[0].message.content
            return app.response_class(
                response=json.dumps({"translated_text": translated_text}, ensure_ascii=False),
                status=200,
                mimetype="application/json")

    return render_template("index.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)