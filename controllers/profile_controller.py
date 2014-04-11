from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import ProfileModel

profile_api = Blueprint('profile_api', __name__)


@profile_api.route("/profile", methods=['GET'])
def api_profile_show():
    return render_template('profile.html')



@profile_api.route("/edit_profile", methods=['GET'])
def api_profile_edit():
    return render_template('edit_profile.html')


# @profile_api.route("/profile/create", methods=['GET'])
# def api_profile_create():
#     return render_template('profile.html', ev={},paras={"action":"create"})


# @profile_api.route("/profile/view/<_eid>", methods=['GET'])
# def api_profile_view(_eid = None):
#     doc = ProfileModel.objects.get(id=_eid)
#     print doc['title']
#     return render_template('profile.html', ev=doc,paras={"action":"view"})

# @profile_api.route("/profile/edit/<_eid>", methods=['GET'])
# def api_profile_edit(_eid = None):
#     doc = ProfileModel.objects.get(id=_eid)
#     return render_template('profile.html', ev=doc,paras={"action":"edit"})


# ######################## APIs BELOW ########################

# @profile_api.route("/api/profile/near/<_eid>/<_dist>", methods=['GET'])
# def api_profile_near(_eid = None, _dist = 10):
#     """ http://mongoengine-odm.readthedocs.org/guide/querying.html#geo-queries """
#     if _eid is not None:
#         ev = ProfileModel.objects.get(id=_eid)
#         LatLng = ev['LatLng']['coordinates']
#         dist = int(_dist)
#         doc = ProfileModel.objects(LatLng__geo_within_center=[[LatLng[0], LatLng[1]],dist])
#         return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
#     else:
#         return '[]'

@profile_api.route("/api/profile/create", methods=['POST'])
def api_profile_post():
    print request
    if request.method == 'POST':
        name = request.json['name']
        gender = request.json['gender']
        age = request.json['age']
        description = request.json['description']
        

        #model = ProfileModel(title=title,description=description,location=location,startTime=startTime,endTime=endTime,userID=userID,latitude=latitude,longitude=longitude,ZIP=ZIP)
        model = ProfileModel(name=name,gender = gender, age = age, description=description)
        doc = model.save()
        print json_util.dumps(doc.to_mongo())
        app.logger.info(doc)
        return json_util.dumps(doc.to_mongo())





# @profile_api.route("/api/profile", methods=['GET'])
# @profile_api.route("/api/profile/<_id>", methods=['GET','POST'])
# def api_profile_getputdelete(_id = None):
#     """ <_id> is for update/delete/get operation"""
#     if(request.method == 'GET'):
#         if _id == None:
#             doc = ProfileModel.objects.all()
#             app.logger.info(doc)
#             return json_util.dumps([d.to_mongo() for d in doc],default=json_util.default)
#         else:
#             doc = ProfileModel.objects.get(id=_id)
#             return json_util.dumps(doc.to_mongo())
#     if(request.method == 'POST'):
#         if(request.json['_method'] == 'DELETE'):
#             print _id;  
#             doc = ProfileModel.objects.get(id=_id)
#             doc.delete()
#             print json_util.dumps(doc.to_mongo())
#             return json_util.dumps(doc.to_mongo())
#         elif(request.json['_method'] == 'PUT'):
#             print _id;  
#             doc = ProfileModel.objects.get(id=_id)
#             #doc.k1 = request.json['k1']
#             doc.save()
#             print json_util.dumps(doc.to_mongo())
#             return json_util.dumps(doc.to_mongo())
