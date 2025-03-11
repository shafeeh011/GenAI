import openai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generateimages/<prompt>")
def generate_images(prompt):
    print('prompt',prompt)
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    print(response)
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)