import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = 'username', 'email'


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Endpoint to create a user
@app.route('user/', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


# endpoint to show all users
@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users) # Convert db objects into json using marshmallow
    return jsonify(result.data)


# endpoint to get a user detail by id
@app.route('/user/<id>', methods=['GET'])
def user_detail(id):
    user = User.query.get(id)
    return users_schema.jsonify(user)


# endpoint to update user
@app.route('/user/<id>', methods=['PUT'])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    user.username = username
    user.email = email

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete the user
@app.route('/user/<id>', methods=['DELETE'])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
