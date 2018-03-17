from flask import Flask, render_template, json, jsonify

app = Flask(__name__, static_folder="../public", template_folder="../public")

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
