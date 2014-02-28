from main import app,db,security

class MongoTestModel(db.Document):
    k1 = db.StringField(required=True)
    k2 = db.StringField()  

class EventModel(db.Document):
    title = db.StringField()
    description = db.StringField()  
    location = db.StringField()  
    time = db.DateTimeField()
    userID = db.StringField()
    ZIP = db.StringField()
    Status = db.StringField()

# no use now
from google.appengine.ext import ndb
class TestModel(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_testmodel(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)