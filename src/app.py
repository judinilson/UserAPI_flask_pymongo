from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost/flaskuserdb"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/api/users", methods=["POST"])
def create_user():
    # receiving data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        id = db.users.insert_one(
            {'username': username, 'password': hashed_password, 'email': email}
        ).inserted_id
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email
        }
        return response
    else:
        return not_found()


@app.route('/api/users',  methods=["GET"])
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/api/users/<id>', methods=["GET"])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/api/users/<id>', methods=["DELETE"])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id), })
    response = jsonify({'message': ' User: ' + id + ' has been deleted'})
    response.status_code = 200
    return response


@app.route('/api/users/<_id>', methods=["PUT"])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        db.users.update_one({
            '_id': ObjectId(_id)},
            {'$set':
             {'username': username,
              'email': email,
              'password': hashed_password
              }
             })
        response = jsonify({'message': 'User ' + _id + 'Updated successfully'})
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True)
