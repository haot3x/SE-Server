from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import MongoTestModel

list_page_api = Blueprint('list_page_api', __name__)

@list_page_api.route("/list_page", methods=['GET'])
def list_page():
    return render_template('list_page.html',models=[])

@list_page_api.route("/list_page/create", methods=['POST'])
def list_page_post():
    print request
    if request.method == 'POST':
        k1 = request.json['k1']
        k2 = request.json['k2']
        model = MongoTestModel(k1=k1,k2=k2)
        doc = model.save()
        print json_util.dumps(doc.to_mongo())
        app.logger.info(doc)
        return json_util.dumps(doc.to_mongo())

@list_page_api.route("/list_page/mongo", methods=['GET'])
@list_page_api.route("/list_page/<_id>", methods=['GET','POST'])
def list_page_getputdelete(_id = None):
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
