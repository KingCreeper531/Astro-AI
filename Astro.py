from flask import Flask, render_template_string, request, redirect
import google.generativeai as genai

app = Flask(__name__)

# ✅ Configure Gemini SDK
genai.configure(api_key="AIzaSyArms8j1J8tlx9ZT4WjX11HnMvR38wflNQ")

# ✅ Load Gemini 2.0 Flash model
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# ✅ Chat history storage
chat_history = []

# ✅ Load HTML (CSS is embedded)
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

# ✅ Main route
@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            response_text = ask_gemini(user_input)
            chat_history.append(("You", user_input))
            chat_history.append(("Astro", response_text))
        elif request.form.get("clear_chat"):
            chat_history = []

    # Build chat history HTML
    history_html = "<div class='chat-history'>"
    for speaker, text in chat_history:
        history_html += f"<p><strong>{speaker}:</strong> {text}</p>"
    history_html += "</div>"

    rendered_page = html_template.replace("{{ history }}", history_html)
    return render_template_string(rendered_page)

if __name__ == "__main__":
    app.run(debug=True)
