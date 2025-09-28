from flask import Flask, render_template
from routes.main import main, slide, lessons, progress, profile, login, register, logout
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Necessário para sessões

# Registrar rotas
app.route("/")(main)
app.route("/slide/<int:slide_number>")(slide)
app.route("/lessons")(lessons)
app.route("/progress")(progress)
app.route("/profile")(profile)
app.route("/login", methods=['GET', 'POST'])(login)
app.route("/register", methods=['GET', 'POST'])(register)
app.route("/logout")(logout)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)