from flask import Blueprint
from flask import request
from flask import render_template
from google.appengine.ext import ndb


from models.testmodel import TestModel

test_api = Blueprint('test_api', __name__)

@test_api.route("/api/test/<test_id>", methods=['GET', 'POST'])
def test_creat(test_id=None):
  """ Return hello template at application root URL."""
  if request.method == 'GET':
    tm = TestModel(parent=ndb.Key("TestModel","yo"),
        content = "dummy content %s " % (test_id))
    tm.put()
    return "{test_id = %s}" % (test_id,)
  else:
    return str(request.data)

@test_api.route("/api/tests", methods=['GET'])
def test_list():
    """ Return hello template at application root URL."""
    ancestor_key = ndb.Key("TestModel","yo")
    tests = TestModel.query_testmodel(ancestor_key).fetch(20)
    tests = TestModel.query().fetch(20)
    #return "</br>".join(test.content for test in tests)
    return render_template('dump_dict_list.html', model_only=True ,dict_list=[i.__dict__ for i in tests])
