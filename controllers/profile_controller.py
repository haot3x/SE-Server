from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import ProfileModel

profile_api = Blueprint('profile_api', __name__)


@profile_api.route("/profile/<_uid>", methods=['GET'])
def api_profile_show(_uid = None):
    doc = ProfileModel.objects.get(_id=_uid)
    return json_util.dumps(doc.to_mongo(), default=json_util.default)



@profile_api.route("/edit_profile", methods=['GET'])
def api_profile_edit():
    return render_template('edit_profile.html')
