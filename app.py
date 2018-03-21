import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_folder="public", template_folder="public")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
api = Api(app)

from models import *

class IndividualPost(Resource):
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

    def get(self, post_id):
        post = BlogPost.query.get(post_id)
        if post:
            post_dict = {
                'id': post.id,
                'title': post.title,
                'body': post.body
            }
            return post_dict, 200
        return { 'error': 'post not found'}, 404

    def delete(self, post_id):
        post = BlogPost.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return {'success':'post {} deleted'.format(post.id)}

    def put(self, post_id):
        data = IndividualPost.parser.parse_args()
        post = BlogPost.query.get(post_id)
        if post is None:
            return { 'error': 'post not found'}, 404
        post.title = data['title']
        post.body  = data['body']
        db.session.commit()
        return {'success': 'post {} updated'.format(post.id)}

class CreatePost(Resource):
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

    def post(self):
        data = CreatePost.parser.parse_args()
        title = data['title']
        body = data['body']
        new_post = BlogPost(title, body)
        db.session.add(new_post)
        db.session.commit()
        return {'title': new_post.title, 'body': new_post.body}, 200


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
        return dict_posts

api.add_resource(IndividualPost, '/post/<int:post_id>')
api.add_resource(PostList, '/posts')
api.add_resource(CreatePost, '/post')

if __name__ == '__main__':
    app.run()

