from flask import Flask, render_template
from routes.main import main, slide
import os

app = Flask(__name__)

# Rotas
app.route("/")(main)
app.route("/slide/<int:slide_number>")(slide)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)