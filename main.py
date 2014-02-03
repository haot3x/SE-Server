""" 
Author: Haotian

main.py is just a top level holding script
different routes are in the handlers directory

"""

import os
import sys
import urllib

# sys.path includes 'server/lib' due to appengine_config.py

from flask import Flask, render_template, url_for
app = Flask(__name__.split('.')[0])

from handlers.event import event_api
app.register_blueprint(event_api)


@app.route('/')
def hello(name="Yale"):
  """ Return hello template at application root URL."""
  return render_template('hello.html', name=name)

@app.route('/admin')
def sitemap():
    # """view all the available RESTful APIs"""
    # links = []
    # for rule in app.url_map.iter_rules():
    # 	links.append(rule.__str__)
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
        
        #l = urllib.unquote("{:50s} {:20s} {}".format(line['endpoint'], line['methods'], line['url']))
        links.append(line)
    #return "</br>".join(links)
    return render_template("sitemap.html", links=links)

if __name__ == '__main__':
    app.debug = True
    app.run()