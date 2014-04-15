from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import EventModel,EventMatchModel

event_api = Blueprint('event_api', __name__)

@event_api.route("/events", methods=['GET'])
def api_event_demo():
    doc = EventModel.objects.all()
    # docs =  json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
    # app.logger.info(docs)
    return render_template('event_list.html',events=doc,paras={"title":"All Events",'action':'all'})


@event_api.route("/event/mine/<_uid>", methods=['GET'])
def api_event_mine(_uid = None):
    doc = EventModel.objects(userID=_uid)
    return render_template('event_list.html',events=doc,paras={"title":"My Events",'action':'mine'})
    #return  json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
    # app.logger.info(docs)
    #return render_template('events.html',events=doc)

@event_api.route("/event/create", methods=['GET'])
def api_event_create():
    return render_template('event.html', ev={},paras={"action":"create"})



#My Requests
@event_api.route("/event/myrequest/<_uid>", methods=['GET'])
def api_event_myrequest(_uid = None):
    match = EventMatchModel.objects().filter(reqUserId = _uid)
    eids = [d.eventId for d in match]


    matchDict = dict((key, value) for (key, value) in [(d.eventId,d.status) for d in match])
    print matchDict
    print eids
    event = EventModel.objects(id__in=eids)
    #return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
    return render_template('event_list.html',events=event,matchDict=matchDict,paras={"title":"My Requests",'action':'myrequest'})

@event_api.route("/event/view/<_eid>", methods=['GET'])
def api_event_view(_eid = None):
    doc = EventModel.objects.get(id=_eid)
    print doc['title']
    return render_template('event.html', ev=doc,paras={"action":"view"})

@event_api.route("/event/edit/<_eid>", methods=['GET'])
def api_event_edit(_eid = None):
    doc = EventModel.objects.get(id=_eid)
    return render_template('event.html', ev=doc,paras={"action":"edit"})


######################## APIs BELOW ########################
@event_api.route("/events/near", methods=['POST'])
def api_event_near():
    """ http://mongoengine-odm.readthedocs.org/guide/querying.html#geo-queries """
    print request
    if request.method == "POST":
        dist = float(request.json['dist'])
        _lat = float(request.json['lat'])
        _lng = float(request.json['lng'])

        doc = EventModel.objects(LatLng__geo_within_center=[[_lat, _lng], dist])
        print len(doc)
        #print json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
        return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
        #return render_template('event_list.html', ev=doc, paras={"action": "radius_refresh"})


@event_api.route("/api/event/create", methods=['POST'])
def api_event_post():
    print request
    if request.method == 'POST':
        title = request.json['title']
        description = request.json['description']
        location = request.json['location']
        startTime = request.json['startTime']
        endTime = request.json['endTime']
        startTime = request.json['startTime']
        userID = request.json['userID']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        ZIP = request.json['ZIP']

        #model = EventModel(title=title,description=description,location=location,startTime=startTime,endTime=endTime,userID=userID,latitude=latitude,longitude=longitude,ZIP=ZIP)
        model = EventModel(title=title,description=description,location=location,startTime=startTime,endTime=endTime,userID=userID,LatLng={"type":"Point","coordinates":[latitude,longitude]},ZIP=ZIP)
        doc = model.save()
        print json_util.dumps(doc.to_mongo())
        app.logger.info(doc)
        return json_util.dumps(doc.to_mongo())





@event_api.route("/api/event", methods=['GET'])
@event_api.route("/api/event/<_id>", methods=['GET','POST'])
def api_event_getputdelete(_id = None):
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
            #doc.k1 = request.json['k1']
            doc.save()
            print json_util.dumps(doc.to_mongo())
            return json_util.dumps(doc.to_mongo())
