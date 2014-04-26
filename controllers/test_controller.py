from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import MongoTestModel

test_api = Blueprint('test_api', __name__)

import webapp2
from google.appengine.api import mail
import smtplib


@test_api.route("/api/tests/email", methods=['GET'])
def test_send_email():
    return send_email("Maxxx <maxxxchou@gmail.com>", "Test Email Feature", """Dear User:

    Your email account has been approved.  You can now visit
    http://www.h-out.com/ and sign in using your Account to
    access new features.

    Please let us know if you have any questions.

    The HOUT Team
    """)

def send_email(_to, _subject, _body):
    mail.send_mail(sender="HOUT-ADMIN <admin@yale-hout.appspotmail.com>",
                  to=_to,
                  subject=_subject,
                  body=_body)
    return 'Email Sent'



@test_api.route("/api/tests/mongo_demo", methods=['GET'])
def test_mongo_demo():
    return render_template('mongo_test.html',models=[])

@test_api.route("/api/tests/mongo/create", methods=['POST'])
def test_mongo_post():
    print request
    if request.method == 'POST':
        k1 = request.json['k1']
        k2 = request.json['k2']
        model = MongoTestModel(k1=k1,k2=k2)
        doc = model.save()
        print json_util.dumps(doc.to_mongo())
        app.logger.info(doc)
        return json_util.dumps(doc.to_mongo())

@test_api.route("/api/tests/mongo", methods=['GET'])
@test_api.route("/api/tests/mongo/<_id>", methods=['GET','POST'])
def test_mongo_getputdelete(_id = None):
    """ <_id> is for update/delete/get operation"""
    if(request.method == 'GET'):
        if _id == None:
            doc = MongoTestModel.objects.all()
            app.logger.info(doc)
            return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
        else:
            doc = MongoTestModel.objects.get(id=_id)
            return json_util.dumps(doc.to_mongo())
    if(request.method == 'POST'):
        if(request.json['_method'] == 'DELETE'):
            print _id;  
            doc = MongoTestModel.objects.get(id=_id)
            doc.delete()
            print json_util.dumps(doc.to_mongo())
            return json_util.dumps(doc.to_mongo())
        elif(request.json['_method'] == 'PUT'):
            print _id;  
            doc = MongoTestModel.objects.get(id=_id)
            k1 = request.json['k1']
            k2 = request.json['k2']
            doc.k1 = k1
            doc.k2 = k2
            doc.save()
            print json_util.dumps(doc.to_mongo())
            return json_util.dumps(doc.to_mongo())
