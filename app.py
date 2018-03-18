import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="public", template_folder="public")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

posts = [
    {
        'id': 1,
        'title': 'first post',
        'body': 'first body'
    },
    {
        'id': 2,
        'title': 'second post',
        'body': 'second body'
    },
    {
        'id': 3,
        'title': 'third post',
        'body': 'third body'
    },
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/post', methods=['POST'])
def create_post():
    request_data = request.get_json()
    new_post = {
        'id': 4,
        'title': request_data['title'],
        'body' : request_data['body']
    }
    posts.append(new_post)
    return jsonify(new_post)

@app.route('/post', methods=['GET'])
def get_posts():
    return jsonify({'posts': posts})

@app.route('/post/<int:id>')
def get_post_by_id(id):
    for post in posts:
        if post['id'] == id:
            return jsonify(post)
    return jsonify({'message': 'post not found'})

if __name__ == '__main__':
    app.run()

