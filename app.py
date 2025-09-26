from flask import Flask, render_template, session, request, redirect, url_for, flash
from routes.main import main, slide, lessons, progress, profile, login, logout, register
from routes.auth import auth_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Registrar blueprints
app.register_blueprint(auth_bp)

# Rotas
app.route("/")(main)
app.route("/slide/<int:slide_number>")(slide)
app.route("/lessons")(lessons)
app.route("/progress")(progress)
app.route("/profile")(profile)
app.route("/login", methods=['GET', 'POST'])(login)
app.route("/logout")(logout)
app.route("/register", methods=['GET', 'POST'])(register)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)