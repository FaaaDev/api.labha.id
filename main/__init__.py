from fileinput import filename
from pickle import TRUE
from unittest import result
from flask import Flask, redirect, request, url_for, jsonify, make_response
from main.shared.shared import db, ma
from main.model.user import User
from main.schema.user import user_schema, users_schema
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/HRISDATA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()


def target_url():
    return "https://itungin.id/"


def response(code, message, status, data):
    return jsonify({
        "code": code,
        "status": status,
        "message": message,
        "data": data
    }, code)


@app.route("/")
def index():
    return redirect(target_url())


@app.route("/v1/api/user", methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        try:
            username = request.json['username']
            phone = request.json['phone']
            email = request.json['email']
            image = ""
            dob = request.json['dob']

            user = User(username, phone, email, image, dob)
            db.session.add(user)
            db.session.commit()
            result = response(200, "Berhasil menambahkan user", True, user_schema.dump(user))
        except IntegrityError:
            db.session.rollback()
            result = response(400, "Email sudah digunakan", False, None)
        finally:
            return result
    else:
        user = User.query.all()

        return response(200, "Berhasil", True, users_schema.dump(user))
    


