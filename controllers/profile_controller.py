from flask import Blueprint
from flask import request
from flask import render_template
from bson import json_util


from main import app,db,security, User
from models.models import ProfileModel

profile_api = Blueprint('profile_api', __name__)

# API for viewing user profile, provide user id in url
@profile_api.route("/profile/view/<_uid>", methods=['GET'])
def api_profile_show(_uid = None):
    try:
        doc = ProfileModel.objects.get(userID=_uid)
        return render_template('profile.html', profile = doc, action = 'exist')
    # in case user don't have profile info
    except Exception,e:
        return render_template('profile.html', action = 'create')
    

# to redirect user to login page
@app.route('/a_page_requires_login')
def login_required_page():
    from flask.ext.security import current_user
    print current_user.id
    userID = str(current_user.id)
    cnt = ProfileModel.objects(userID=userID).count()
    #print "cnt"
    #print cnt
    
    #return render_template('landing.html')
    if cnt == 0:
        doc = User.objects.get(id=userID)
        name = doc.first_name + " " + doc.last_name
        age = str(doc.age)
        gender = doc.gender
        description=""

        doc2 = ProfileModel(name=name,gender=gender,age=age,description=description,userID=userID,image=None)
        doc2.save()    
    return render_template('landing.html')    

# API for profile creation
@profile_api.route("/profile/create/<_uid>", methods=['GET'])
def api_profile_create(_uid = None):
    return render_template('edit_profile.html', action='create')
    

#API for profile modification
@profile_api.route("/profile/edit/<_uid>", methods=['GET'])
def api_profile_edit(_uid = None):
    try:
        doc = ProfileModel.objects.get(userID=_uid)
        return render_template('edit_profile.html', profile = doc, action='edit')
    except Exception,e:
        pass


# API for profile image handling
@profile_api.route("/api/profile/image/<_uid>", methods=['POST'])
def api_profile_image(_uid = None):
    cnt = ProfileModel.objects(userID=_uid).count()
    if cnt == 1:
        doc = ProfileModel.objects.get(userID=_uid)
        try:
            # img = request.files['img']
            # doc.photo.put(img, content_type = 'image/jpeg') 
            doc.image = request.json['image']
            # print(doc.image)
            doc.save();

        except Exception, e:
            print e
            return str(e)
    else:
        image = request.json['image']
        model = ProfileModel(image=image, userID=_uid)
        doc = model.save()
  
    return json_util.dumps(doc.to_mongo())


# API for profile create, parameters passed by AJAX
@profile_api.route("/api/profile/create", methods=['POST'])
def api_profile_post():
    print request
    _method = request.json['_method']
    userID = request.json['userID'] 
    cnt = ProfileModel.objects(userID=userID).count()
    if _method == 'POST' and cnt == 0:
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
    elif _method == 'PUT' or cnt == 1:
        userID = request.json['userID']
        doc = ProfileModel.objects.get(userID=userID)

        name = request.json['name']
        gender = request.json['gender']
        age = request.json['age']
        description = request.json['description']

        if not name is None or name == '':
            doc.name = name
        if not gender is None or gender == '':
            doc.gender = gender
        if not age is None or age == '':
            doc.age = age
        if not description is None or description == '':
            doc.description = description

        doc.save()
        return json_util.dumps(doc.to_mongo())
    return 1