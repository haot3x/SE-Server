from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import EventMatchModel, EventModel, ProfileModel

from flask.ext.security import current_user

from mongoengine.queryset import Q

import random, string

eventmatch_api = Blueprint('eventmatch_api', __name__)


def randomstring(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

@eventmatch_api.route("/matches", methods=['GET'])
def api_eventmatch_dump():
	doc = EventMatchModel.objects.all()
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)

#my matched events
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

@eventmatch_api.route("/match/incoming/<_eventid>", methods=['GET'])
def eventmatch_view_joins(_eventid = None):
	doc = EventMatchModel.objects(eventId=_eventid)
	return json_util.dumps([d.to_mongo() for d in doc], default=json_util.default)

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

@eventmatch_api.route("/match/createtest", methods=['GET'])
def eventmatch_test():
	eventId = "e2"
	eventOwnerId = "u5"
	reqUserId = "u1"
	m = EventMatchModel(eventId=eventId,eventOwnerId=eventOwnerId,reqUserId=reqUserId)
	m.save()
	return json_util.dumps(m.to_mongo())


@eventmatch_api.route("/match/join/request", methods=['POST'])
def eventmatch_join_request():
    cnt = ProfileModel.objects(userID=str(current_user.id)).count()
    if cnt == 0:
    	raise Exception("no profile")
    else:
		eventId = request.json['eventId']
		eventOwnerId = request.json['eventOwnerId']
		reqUserId = request.json['reqUserId']

		model = EventMatchModel(eventId=eventId, eventOwnerId=eventOwnerId, reqUserId=reqUserId)
		doc = model.save()
		print json_util.dumps(doc.to_mongo())
		app.logger.info(doc)
		return json_util.dumps(doc.to_mongo())

