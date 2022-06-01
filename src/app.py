from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

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
        {'message': 'received'}


if __name__ == '__main__':
    app.run(debug=True)
