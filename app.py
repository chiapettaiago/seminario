from flask import Flask, render_template
from routes.main import main

app = Flask(__name__)

main = app.route("/")(main)

if __name__ == "__main__":
    app.run(debug=True)