from flask import Flask, render_template, request, jsonify  
from flask_cors import CORS  # Import CORS
import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is missing from .env file! Please add it to your .env file.")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

app = Flask(__name__)
CORS(app)  # Allow frontend to connect to backend

@app.route("/")
def landing():
    return render_template("landing.html")  # Default page is landing.html

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")  # Show chatbot page on GET request
    
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Please enter a message!"}), 400

        payload = {"contents": [{"parts": [{"text": user_input}]}]}

        response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()
        data = response.json()

        generated_content = ""
        if "candidates" in data and data["candidates"]:
            first_candidate = data["candidates"][0]
            if "content" in first_candidate:
                content_parts = first_candidate["content"].get("parts", [])
                if content_parts:
                    generated_content = content_parts[0].get("text", "")

        return jsonify({"response": generated_content or "No response received from API."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"HTTP error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

