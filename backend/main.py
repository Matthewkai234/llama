from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import requests
from dotenv import load_dotenv
import os

load_dotenv()

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

cred = credentials.Certificate("C:\\Users\\the-r\\Desktop\\Llama\\backend\\serviceAccountKey.json") 
firebase_admin.initialize_app(cred)
app = Flask(__name__)
CORS(app)
print("API KEY:", FIREBASE_API_KEY)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User created", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        resp = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
            json=payload
        )
        if resp.status_code == 200:
            return jsonify(resp.json()), 200
        else:
            return jsonify({"error": resp.json()}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chatbot route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    reply_to = data.get("reply_to")  # ✅ No indentation issue here

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if reply_to is not None:  # ✅ Handles empty string, null, etc.
        bot_response = f"meow! (in response to: {reply_to})"
    else:
        bot_response = f"You said: {user_message}"

    return jsonify({"response": bot_response}), 200


# Test route
@app.route("/")
def index():
    return "Try POSTing to /signup, /login or /chat 😎"

if __name__ == "__main__":
    app.run(debug=True)
