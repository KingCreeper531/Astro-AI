from flask import Flask, render_template_string, request
import google.generativeai as genai
import os

app = Flask(__name__)

# ✅ Load Gemini API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Load Gemini 2.0 Flash model
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# ✅ Chat history storage
chat_history = []

# ✅ Load HTML template with embedded CSS
with open("Astro.html", "r") as f:
    html_template = f.read()

# ✅ Streaming Gemini response
def ask_gemini(prompt):
    try:
        stream = chat.send_message(prompt, stream=True)
        response_text = ""
        for chunk in stream:
            response_text += chunk.text
        return response_text
    except Exception as e:
        return f"Error: {e}"

# ✅ Flask route with chat history and clear button
@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    if request.method == "POST":
        if request.form.get("clear_chat"):
            chat_history = []
        else:
            user_input = request.form.get("user_input")
            if user_input:
                response_text = ask_gemini(user_input)
                chat_history.append(("You", user_input))
                chat_history.append(("Astro", response_text))

    # Build chat history HTML
    history_html = "<div class='chat-history'>"
    for speaker, text in chat_history:
        history_html += f"<p><strong>{speaker}:</strong> {text}</p>"
    history_html += "</div>"

    rendered_page = html_template.replace("{{ history }}", history_html)
    return render_template_string(rendered_page)

if __name__ == "__main__":
    app.run(debug=True)
