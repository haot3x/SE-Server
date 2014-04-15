from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security
from models.models import ProfileModel

profile_api = Blueprint('profile_api', __name__)


@profile_api.route("/profile/view/<_uid>", methods=['GET'])
def api_profile_show(_uid = None):
    try:
        doc = ProfileModel.objects.get(userID=_uid)
        return render_template('profile.html', profile = doc, action = 'exist')
    except Exception,e:
        #TODO: clean up here
        #for first time create
        return render_template('profile.html', action = 'create')
    


@profile_api.route("/profile/create/<_uid>", methods=['GET'])
def api_profile_create(_uid = None):
    return render_template('edit_profile.html', action='create')
    


@profile_api.route("/profile/edit/<_uid>", methods=['GET'])
def api_profile_edit(_uid = None):
    try:
        doc = ProfileModel.objects.get(userID=_uid)
        return render_template('edit_profile.html', profile = doc, action='edit')
    except Exception,e:
        pass

# ######################## APIs BELOW ########################


@profile_api.route("/api/profile/create", methods=['POST'])
def api_profile_post():
    print request
    _method = request.json['_method']

    if _method == 'POST':
        name = request.json['name']
        gender = request.json['gender']
        age = request.json['age']
        description = request.json['description']
        userID = request.json['userID']        

        #model = ProfileModel(title=title,description=description,location=location,startTime=startTime,endTime=endTime,userID=userID,latitude=latitude,longitude=longitude,ZIP=ZIP)
        model = ProfileModel(name=name,gender = gender, age = age, description=description, userID=userID)
        doc = model.save()
        print json_util.dumps(doc.to_mongo())
        app.logger.info(doc)
        return json_util.dumps(doc.to_mongo())
    elif _method == 'PUT':
        userID = request.json['userID']
        doc = ProfileModel.objects.get(userID=userID)

        name = request.json['name']
        gender = request.json['gender']
        age = request.json['age']
        description = request.json['description']

        if not name is None or name == '':
            print "heheehehehe"
            doc.name = name
        if not gender is None or gender == '':
            doc.gender = gender
        if not age is None or age == '':
            doc.age = age
        if not description is None or description == '':
            doc.description = description

        doc.save()
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
