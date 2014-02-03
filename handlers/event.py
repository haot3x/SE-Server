from flask import Blueprint

event_api = Blueprint('event_api', __name__)

@event_api.route("/event/<eid>")
def event(eid=None):
  """ Return hello template at application root URL."""
  return "{eid=%s}" % (eid,)
