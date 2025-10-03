from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os, uuid, datetime

app = Flask(__name__)
chat_history = []
session_id = str(uuid.uuid4())  # Unique session ID

# Configure Gemini API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

@app.route("/")
def index():
    return render_template("Astro.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json["message"]
    chat_history.append({"role": "user", "text": user_input})

    try:
        response = chat.send_message(user_input, stream=True)
        full_response = ""

        for chunk in response:
            if chunk.text:
                full_response += chunk.text

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_history.append({
            "role": "model",
            "text": full_response,
            "timestamp": timestamp
        })

        return jsonify({
            "response": full_response,
            "timestamp": timestamp,
            "session": session_id
        })

    except Exception as e:
        return jsonify({
            "response": "Oops! Astro AI encountered an error.",
            "error": str(e),
            "session": session_id
        }), 500

@app.route("/clear", methods=["POST"])
def clear():
    chat_history.clear()
    return jsonify({"status": "cleared", "session": session_id})

# Bind to 0.0.0.0 and dynamic port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
