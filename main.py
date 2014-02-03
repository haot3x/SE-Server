""" 
Author: Haotian

main.py is just a top level holding script
different routes are in the handlers directory

local install:
    sudo pip install flask-security -t /Users/Ted/Code/SE-Server/server/lib

"""

import os
import sys
import urllib

# sys.path includes 'server/lib' due to appengine_config.py

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

from flask.ext.security import Security

app = Flask(__name__.split('.')[0])
app.config['DEBUG'] = True
app.config['SECURITY_REGISTERABLE'] = True

from handlers.event import event_api
app.register_blueprint(event_api)

@app.route('/')
def hello():
  """ Return hello template at application root URL."""
  return render_template('hello.html', name="Yale HOUT")


@app.route('/api')
def sitemap():
    links = []
    for rule in app.url_map.iter_rules():
        line = {}
        line['endpoint'] = rule.endpoint;
        line['methods'] = ",".join(rule.methods)
        opts = {}
        for arg in rule.arguments:
            opts[arg] = "[{0}]".format(arg)
        url = url_for(rule.endpoint, **opts)
        line['url'] = urllib.unquote(url)
        
        #links.append(urllib.unquote("{:50s} {:20s} {}".format(line['endpoint'], line['methods'], line['url'])))
        links.append(line)
    #return "</br>".join(links)
    return render_template("sitemap.html", links=links)
