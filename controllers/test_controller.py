from flask import Blueprint
from flask import request
from flask import render_template
from google.appengine.ext import ndb

from flask import json

from models.models import TestModel

test_api = Blueprint('test_api', __name__)

@test_api.route("/api/tests/<test_id>", methods=['GET', 'POST'])
def test_creat(test_id=None):
  """ Test """
  if request.method == 'GET':
    tm = TestModel(parent=ndb.Key("TestModel","yo"),
        content = "dummy content %s " % (test_id))
    tm.put()
    return "{test_id = %s}" % (test_id,)
  else:
    return str(request.data)

@test_api.route("/api/tests", methods=['GET'])
def test_list():
    """ Test """
    ancestor_key = ndb.Key("TestModel","yo")
    tests = TestModel.query_testmodel(ancestor_key).fetch(20)
    tests = TestModel.query().fetch(20)
    return json.dumps([p.to_dict() for p in list(tests)])
    #return render_template('dump_dict_list.html', model_only=True ,dict_list=[i.__dict__ for i in tests])

@test_api.route("/api/tests/random", methods=['GET','DELETE'])
def test_random():
    """ Test """
    import random
    x = random.randint(0,1000)
    y = random.randint(0,1000)
    return '{"a":%s, "b":%s}' % (x,y)

@test_api.route("/api/tests/sec", methods=['GET'])
def test_sec():
    """ Test """
    return '{"a":%s, "b":%s}' % (x,y)

