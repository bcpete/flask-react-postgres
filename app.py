import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="public", template_folder="public")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#from models import User

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()

