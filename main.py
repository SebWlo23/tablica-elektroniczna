
from flask import Flask, redirect, render_template, request, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from base64 import b64decode
from io import StringIO, BytesIO

import ftplib


app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="SebWlo23",
    password="alamakota",
    hostname="SebWlo23.mysql.pythonanywhere-services.com",
    databasename="SebWlo23$Tablica4",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 # connection timeouts
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # no warning disruptions

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    availability = db.Column(db.String(4096))
    information = db.Column(db.String(4096))
    photo = db.Column(db.String(4096))
    email = db.Column(db.String(4096))
    side = db.Column(db.String(4096))
    def __init__(self, name, availability, information, photo, email, side):
        self.name = name
        self.availability = availability
        self.information = information
        self.photo = photo
        self.email = email
        self.side = side

class UsersSchema(ma.Schema):
    class Meta:

        fields = ('id' ,'name' ,'availability' ,'information', 'photo', 'email', 'side')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


@app.route("/users", methods=["GET"])
def get_all_users():
    user_many = Users.query.all()
    result = users_schema.dump(user_many)
    return jsonify(result)


@app.route("/user/<id>", methods=["GET"])
def get_all_user(id):
    user = Users.query.get(id)
    result = user_schema.dump(user)
    print(user.information)
    return jsonify(result)


@app.route("/users", methods=["POST"])
def add_user():
    name = request.json["name"]
    availability = request.json["availability"]
    information = request.json["information"]
    photo = request.json["photo_name"]
    email = request.json["email"]
    side = request.json["side"]
    new_user = Users(name, availability, information, photo, email, side)
    db.session.add(new_user)
    db.session.commit()
    user = Users.query.get(new_user.id)
    upload_file_to_ftp(request.json["photo_name"], request.json["photo"])
    return user_schema.jsonify(user)

@app.route("/users/last", methods=["GET"])
def get_last_user():
    user_many = Users.query.all()
    last_user = user_many[-1]
    result = user_schema.dump(last_user)
    return jsonify(result)

@app.route('/user/put/<id>', methods=['PUT'])
def update_users(id):
    user = Users.query.get(id)
    name = request.json["name"]
    availability = request.json["availability"]
    information = request.json["information"]
    photo = request.json["photo"]
    email = request.json["email"]
    side = request.json["side"]
    user.name = name
    user.availability = availability
    user.information = information
    user.photo = photo
    user.email = email
    user.side = side
    db.session.commit()
    upload_file_to_ftp(request.json["photo_name"], request.json["photo"])
    return user_schema.jsonify(user)

@app.route("/user/email/<email>", methods=["GET"])
def get_mail(email):
    user = Users.query.filter_by(email=email).one_or_404()
    result = user_schema.dump(user)
    print(user.information)
    return jsonify(result)


##################################################################################3

class Devices(db.Model):

    __tablename__ = "device"
    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(4096))
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(4096))
    refresch = db.Column(db.Integer)
    def __init__(self, adress, user_id, name, refresch):
        self.adress = adress
        self.user_id = user_id
        self.name = name
        self.refresch = refresch


class DevicesSchema(ma.Schema):
    class Meta:

        fields = ('id' ,'adress' ,'user_id' ,'name', 'refresch')


device_schema = DevicesSchema()
devices_schema = DevicesSchema(many=True)


@app.route("/devices", methods=["GET"])
def get_all_devices():
    device_many = Devices.query.all()
    result = devices_schema.dump(device_many)
    return jsonify(result)


@app.route("/device/<id>", methods=["GET"])
def get_all_device(id):
    device = Devices.query.get(id)
    result = device_schema.dump(device)
    return jsonify(result)


@app.route("/devices", methods=["POST"])
def add_device():
    adress = request.json["adress"]
    user_id = request.json["user_id"]
    name = request.json["name"]
    refresch = request.json["refresch"]
    new_device = Devices(adress, user_id, name, refresch)
    db.session.add(new_device)
    db.session.commit()
    device = Devices.query.get(new_device.id)
    return device_schema.jsonify(device)


@app.route('/device/put/<id>', methods=['PUT'])
def update_devices(id):
    device = Devices.query.get(id)
    user_id = request.json['user_id']
    refresch = request.json['refresch']
    device.user_id = user_id
    device.refresch = refresch
    db.session.commit()
    return device_schema.jsonify(device)

def upload_file_to_ftp(filename, file_content):
    content_bytes = b64decode(file_content)
    file_stream = BytesIO(content_bytes)

    with ftplib.FTP("157.230.104.175") as ftp:
        ftp.login("sba", "sba1")
        ftp.storbinary(f"STOR {filename}", file_stream)












###############################################################################################################


