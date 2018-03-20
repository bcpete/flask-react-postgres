import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="public", template_folder="public")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from models import *

@app.route('/')
def home():
    return render_template("index.html")

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
        type=str,
        required=True,
        help="this field cant be blank"
    )
    parser.add_argument('body',
        type=str,
        required=True,
        help="this field cant be blank"
    )

    def get(self, title):
        post = next(filter(lambda x: x['title'] == title, posts), None)
        return {'post': post}, 200 if post else 404

    def post(self, title):

        data = Post.parser.parse_args()
        title = data['title']
        body = data['body']
        new_post = BlogPost(title, body)
        
        post_add=new_post.add(new_post)
        if post_add:
            return {'title': new_post.title, 'body': new_post.body}, 200
        else:
            return {'error': 'did not work'}, 500

    def delete(self, title):
        global posts
        posts = list(filter(lambda x: x['title'] != title, posts))
        return {'success':'post deleted'}

    def put(self, title):
        data = Post.parser.parse_args()
        post = next(filter(lambda x: x['title'] == title, posts), None)
        if post is None:
            return {'error': 'post not found'}, 404
        else:
            post.update(data)
            return post

class PostList(Resource):
    def get(self):
        posts = BlogPost.query.all()
        dict_posts = []
        for post in posts:
            dict = {
                'id': post.id,
                'title': post.title,
                'body':post.body
            }
            dict_posts.append(dict)
        print(dict_posts)
        return dict_posts

api.add_resource(Post, '/post/<string:title>')
api.add_resource(PostList, '/posts')

if __name__ == '__main__':
    app.run()

