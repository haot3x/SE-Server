from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import EventModel

event_api = Blueprint('event_api', __name__)

@event_api.route("/events", methods=['GET'])
def test_mongo_demo():
    doc = EventModel.objects.all()
    # docs =  json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
    # app.logger.info(docs)
    return render_template('events.html',events=doc)

@event_api.route("/api/event/create", methods=['GET'])
def test_mongo_post():
    model = EventModel(title = 'hout',description = 'yoyo')
    doc = model.save()
    print json_util.dumps(doc.to_mongo())
    app.logger.info(doc)
    return json_util.dumps(doc.to_mongo())

@event_api.route("/api/event", methods=['GET'])
@event_api.route("/api/event/<_id>", methods=['GET','POST'])
def test_mongo_getputdelete(_id = None):
    """ <_id> is for update/delete/get operation"""
    if(request.method == 'GET'):
        if _id == None:
            doc = EventModel.objects.all()
            app.logger.info(doc)
            return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
        else:
            doc = EventModel.objects.get(id=_id)
            return json_util.dumps(doc.to_mongo())
    if(request.method == 'POST'):
        if(request.json['_method'] == 'DELETE'):
            print _id;  
            doc = EventModel.objects.get(id=_id)
            doc.delete()
            print json_util.dumps(doc.to_mongo())
            return json_util.dumps(doc.to_mongo())
        elif(request.json['_method'] == 'PUT'):
            print _id;  
            doc = EventModel.objects.get(id=_id)
            k1 = request.json['k1']
            k2 = request.json['k2']
            doc.k1 = k1
            doc.k2 = k2
            doc.save()
            print json_util.dumps(doc.to_mongo())
            return json_util.dumps(doc.to_mongo())
