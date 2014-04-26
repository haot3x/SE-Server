from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import EventMatchModel, EventModel, ProfileModel

from flask.ext.security import current_user

from mongoengine.queryset import Q
from twilio.rest import TwilioRestClient 

import random, string

eventmatch_api = Blueprint('eventmatch_api', __name__)

# for testing purpose only
def randomstring(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

# API for viewing all match records
@eventmatch_api.route("/matches", methods=['GET'])
def api_eventmatch_dump():
	doc = EventMatchModel.objects.all()
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)

# API for viewing my matched events
@eventmatch_api.route("/match/mine/<_userid>", methods=['GET'])
def eventmatch_mine(_userid = None):
	doc = EventMatchModel.objects(Q(eventOwnerId=_userid, status="matched") | Q(reqUserId=_userid, status="matched"))
	
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)

'''
#all requester for my event1
@eventmatch_api.route("/match/mine/requesters/eventid=<_eventid>&eventownerid=<_eventownerid>", methods=['GET'])
def eventmatch_num_requesters(_eventid = None, _eventownerid = None):
	doc = EventMatchModel.objects(eventId=_eventid, eventOwnerId=_eventownerid)
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)

'''
# API for viewing all incoming reuqest for a certain event
@eventmatch_api.route("/match/incoming/<_eventid>", methods=['GET'])
def eventmatch_view_joins(_eventid = None):
	doc = EventMatchModel.objects(eventId=_eventid)
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)

# API to accept a request form a certain requester
@eventmatch_api.route("/match/accept", methods=['POST'])
def eventmatch_test_accept():
	print request
	if request.method == "POST":
		_eventid = request.json['eventId']
		_requserid = request.json['reqUserId']

		doc = EventMatchModel.objects(eventId=_eventid)
		doc2 = EventModel.objects.get(id=_eventid)
		print doc
		for d in doc:
			if (d.reqUserId == _requserid):
				d.status = "matched"
				doc2.status = "closed"
				doc2.save()
			else:
				d.status = "declined"
			d.save()
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)


@eventmatch_api.route("/sendSMS/<_number>/<_message>", methods=['GET'])
def eventmatch_sendSMS(_number = None, _message = None):
	
	ACCOUNT_SID = "AC7be7eca91ee23111d924d090a70fa933" 
	AUTH_TOKEN = "c78ca17ad1777ca6de9d3f3844dbc1e6" 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	try: 
		client.messages.create( 
			to=_number,
			from_="2036803816", 
			body=_message  
		)
		return 'Message Sent'
	except Exception,e:
		return str(e)

@eventmatch_api.route("/SMSAccept", methods=['POST'])
def eventmatch_SMSAccpet():
	print request
	_eventid = request.json['eventId']
	_requesterid = request.json['reqUserId']
	_hostid = request.json['hostId']
	doc1 = ProfileModel.objects.get(userID = _requesterid)
	doc2 = ProfileModel.objects.get(userID = _hostid)
	doc3 = EventModel.objects.get(id=_eventid)

	ACCOUNT_SID = "AC7be7eca91ee23111d924d090a70fa933" 
	AUTH_TOKEN = "c78ca17ad1777ca6de9d3f3844dbc1e6" 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	
	try: 
		# To the reqeuster
		client.messages.create( 
			to=doc1.phone,
			from_="+12036803816", 
			body="Your Event Request: " + doc3.title + " With " + doc2.name + 
				" is accepted. You will be meeting at " + doc3.location 
				+ " "+ doc3.startTime + " HOUT TEAM MESSAGE"
		)

		client.messages.create( 
			to=doc2.phone,
			from_="+12036803816", 
			body="Your Event: " + doc3.title + " With " + doc1.name + 
				" is confirmed. You will be meeting at " + doc3.location 
				+ ". "+ doc3.startTime+ " -- HOUT TEAM MESSAGE"
		)

		# To the Host
		return 'Message Sent'
	except Exception,e:
		return str(e)

@eventmatch_api.route("/match/createtest", methods=['GET'])
def eventmatch_test():
	eventId = "e2"
	eventOwnerId = "u5"
	reqUserId = "u1"
	m = EventMatchModel(eventId=eventId,eventOwnerId=eventOwnerId,reqUserId=reqUserId)
	m.save()
	return json_util.dumps(m.to_mongo())

# API to send a join request for a certain event
@eventmatch_api.route("/match/join/request", methods=['POST'])
def eventmatch_join_request():
    cnt = ProfileModel.objects(userID=str(current_user.id)).count()
    if cnt == 0:
    	raise Exception("no profile")
    else:
    	eventId = request.json['eventId']
    	eventOwnerId = request.json['eventOwnerId']
    	reqUserId = request.json['reqUserId']
    	count = EventMatchModel.objects(eventId=eventId, eventOwnerId=eventOwnerId, reqUserId=reqUserId).count()
    	if count == 0:
    		model = EventMatchModel(eventId=eventId, eventOwnerId=eventOwnerId, reqUserId=reqUserId)
    		doc = model.save()
    		print json_util.dumps(doc.to_mongo())
    		app.logger.info(doc)
    		return json_util.dumps(doc.to_mongo())
    	else:
    		pass

