from flask import Blueprint

event_api = Blueprint('event_api', __name__)

@event_api.route("/event/<eid>", methods=['GET', 'POST'])
def event(eid=None):
  """ Return hello template at application root URL."""
  if request.method == 'GET':
    return "{eid=%s}" % (eid,)  
  else:
    return "eid is a number"
  
