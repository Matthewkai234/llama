from flask import Flask, request, Response, jsonify, stream_with_context
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import requests
from dotenv import load_dotenv
import os
import re
import asyncio
import httpx
import json

history = []
OLLAMA_BASE_URL = "http://localhost:11434"

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

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid email format"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

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

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid email format"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    reply_to = data.get("reply_to")  

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if reply_to is not None: 
        bot_response = f"meow! (in response to: {reply_to})"
    else:
        bot_response = f"You said: {user_message}"

    return jsonify({"response": bot_response}), 200



@app.route("/ollama", methods=["POST"])
def chat_with_ollama():
    data = request.get_json()
    model = data.get("model")
    message = data.get("message")

    if not model or not message:
        return jsonify({"error": "Model and message are required"}), 400

    user_message = {"role": "user", "content": message}
    history.append(user_message)

    async def async_generate():
        yield ": stream started\n\n"
        assistant_response = ""

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("POST", f"{OLLAMA_BASE_URL}/api/chat", json={
                    "model": model,
                    "messages": history,
                    "stream": True
                }) as response:
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        if line.strip() == "data: [DONE]":
                            break
                        if line.startswith("data: "):
                            payload = json.loads(line.removeprefix("data: "))
                            chunk = payload["message"]["content"]
                            assistant_response += chunk
                            yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            history.append({"role": "assistant", "content": assistant_response})
            yield "data: [DONE]\n\n"
        except Exception as e:
            print("Error while communicating with Ollama:", e)
            yield f"data: {json.dumps({'error': 'Streaming failed'})}\n\n"

    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_gen = async_generate()

        try:
            while True:
                chunk = loop.run_until_complete(async_gen.__anext__())
                yield chunk
        except StopAsyncIteration:
            pass
        finally:
            loop.close()

    return Response(stream_with_context(generate()), mimetype="text/event-stream")



@app.route("/clear-history", methods=["POST"])
def clear_history():
    history.clear()
    return jsonify({"success": True})


# Test route
@app.route("/")
def index():
    return "Try POSTing to /signup, /login or /chat 😎"

if __name__ == "__main__":
    app.run(debug=True)
