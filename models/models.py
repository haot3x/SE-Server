from main import app,db,security
import datetime

class MongoTestModel(db.Document):
    k1 = db.StringField(required=True)
    k2 = db.StringField()

class EventModel(db.Document):
    title = db.StringField()
    description = db.StringField()  
    createTime = db.DateTimeField(default=datetime.datetime.now)
    startTime = db.StringField()
    endTime = db.StringField()
    userID = db.StringField()
    location =  db.StringField()
    # latitude = db.FloatField()  
    # longitude = db.FloatField()
    LatLng = db.PointField()
    ZIP = db.StringField()
    status = db.StringField(default='new')


class ProfileModel(db.Document):
    name = db.StringField()
    gender = db.StringField()
    description = db.StringField()

class EventMatchModel(db.Document):
    eventId = db.StringField()
    eventOwnerId = db.StringField()
    reqUserId = db.StringField()
    status = db.StringField(default='open')


# no use now
from google.appengine.ext import ndb
class TestModel(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_testmodel(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)

