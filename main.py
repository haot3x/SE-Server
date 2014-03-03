""" 
Author: Haotian

main.py is just a top level holding script
different routes are in the handlers directory

local install:
    sudo pip install flask-security -t /Users/Ted/Code/SE-Server/server/lib
    sudo pip install -r requirements.txt -t /Users/Ted/Code/SE-Server/server/lib


gmail
    yale.hout@gmail.com
    yalese14

https://mongolab.com/databases/yalehout/collections/
    yale.hout@gmail.com
    qwe123

mongo ds063307.mongolab.com:63307/yalehout -u yalehout -p qwe123
mongodb://yalehout:qwe123@ds063307.mongolab.com:63307/yalehout


"""

import os
import sys
import urllib

# sys.path includes 'server/lib' due to appengine_config.py

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import redirect

from flask.ext.security import Security,UserMixin, RoleMixin, login_required
from flask.ext.login import LoginManager 
from google.appengine.ext import ndb

from flask import Flask, render_template
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required


from flask_wtf import Form
from wtforms import TextField, BooleanField,IntegerField
from wtforms.validators import Required
from flask_mail import Mail


from flask_security.forms import RegisterForm

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])
    gender = TextField('Gender', [Required()])
    age = IntegerField('Age', [Required()])



app = Flask(__name__.split('.')[0])
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_POST_LOGIN_VIEW'] = 'a_page_requires_login'


# # At top of file
# from flask_mail import Mail
# # After 'Create app'
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'yale.hout@gmail.com'
# app.config['MAIL_PASSWORD'] = 'yalese14'
# mail = Mail(app)


# Flask Configuration goes here
# http://pythonhosted.org/Flask-Security/configuration.html
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

# MongoDB Configuration goes here
app.config["MONGODB_SETTINGS"] = {'DB': "yalehout", "host":'mongodb://yalehout:qwe123@ds063307.mongolab.com:63307/yalehout'}
# if localhost - make sure you start the daemon first - mongod
# app.config['MONGODB_DB']='test'
# app.config['MONGODB_HOST']='127.0.0.1'
# app.config['MONGODB_PORT']=27017
db = MongoEngine(app)



class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    
    #above is the minimum, dont touch

#http://pythonhosted.org/Flask-Security/customizing.html
class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    
    # #above is the minimum, dont touch
    last_name = db.StringField(max_length=255)
    first_name = db.StringField(max_length=255)
    gender = db.StringField(max_length=255)
    age = db.IntField()
    # user_prof_id = db.ReferenceField("")
    

user_datastore = MongoEngineUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
security = Security(app, user_datastore,register_form=ExtendedRegisterForm)

from controllers.test_controller import test_api
app.register_blueprint(test_api)

from controllers.event_controller import event_api
app.register_blueprint(event_api)

# @app.before_first_request
# def create_user():
#     user_datastore.create_user(email='test@yale.edu', password='qwe123')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def hello():
    return render_template('landing.html')


@app.route('/events_old')
def events():

    from random import randint 
    def m():
        m.id = randint(1,1000)
        m.name = 'bar %s' % (randint(1,1000),)
        m.time = 'time %s' % (randint(1,1000),)

    #l = [m().__dict__ for i in xrange(1,100)]
    
    for i in xrange(1,100):
        t = m()
        l.append(t.__dict__)

    return render_template('list_page.html',events=l)


@app.route('/basic')
def basic():
    return render_template('basic.html')



@app.route('/a_page_requires_login')
@login_required
def login_required_page():
    return render_template('a_page_requires_login.html')


@app.route('/api')
def sitemap():
    links = []
    for rule in app.url_map.iter_rules():
        line = {}
        line['endpoint'] = rule.endpoint;
        line['methods'] = ",".join(sorted(rule.methods))
        opts = {}
        for arg in rule.arguments:
            opts[arg] = "[{0}]".format(arg)
        url = url_for(rule.endpoint, **opts)
        line['url'] = urllib.unquote(url)
        
        #links.append(urllib.unquote("{:50s} {:20s} {}".format(line['endpoint'], line['methods'], line['url'])))
        links.append(line)
    #return "</br>".join(links)
    li = sorted(links, key=lambda k: k['url'])
    return render_template("api.html", links=li)
