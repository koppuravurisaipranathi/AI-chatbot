from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# You can change to other Together-supported models like mistralai/Mistral-7B-Instruct-v0.1
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    print(f"User message: {user_message}")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a kind and supportive mental health assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload
        )
        print("🔍 RAW RESPONSE:", response.text)

        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print(f"✅ Bot reply: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ Together.ai API Error: {e}")
        return jsonify({"reply": f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
