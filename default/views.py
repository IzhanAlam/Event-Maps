from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from default.models import userEvent, geo, eventInfo, geo30min, geo2hrs, geo6hrs, geoprivate, privateComments
from django.utils import timezone
from geojson import Point, Feature, FeatureCollection, dump
import geojson
from django.http import JsonResponse
import json
import datetime

# Default Page
def index(request):
    return render(request,'default/index.html')

#Sign Up Page
def sign_up(request):
    return render(request,'default/sign_up.html')

def acc_created(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        email = request.POST.get('email')
        if (user_name and email and pass_word) != (None):
            user = User.objects.filter(username=user_name)
            email_text = User.objects.filter(email=email)
            if user.exists():
                return render(request, 'default/sign_up.html', {'message':'Username in use'})
            if email_text.exists():
                return render(request, 'default/sign_up.html', {'message':'E-mail in use'})
            else:
                new_user = User.objects.create_user(username=user_name, email = email, password=pass_word)
                new_user.save()
                return render(request, 'default/index.html', {'message':'Account Created'})
        else:
            return render(request, 'default/sign_up.html', {'message':'One or more entries empty'})
    else:
        return render(request,'default/sign_up.html')

def logged_in(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user2 = User.objects.filter(username=user_name)
        if user2:
            user = User.objects.get(username=user_name)
            account = authenticate(request, username=user_name, password=pass_word)
            check_pass = user.check_password(pass_word)
            if check_pass:
                user_true = True
                login(request, account)
                return render (request, 'default/index.html', {'user_true': user_true, 'message': 'Signed in.'})
            else:
                user_true = False
                return render (request, 'default/index.html', {'user_true': user_true, 'message':'Incorrect Username/Password.'})
        else:
            user_true = False
            return render (request, 'default/index.html', {'user_true': user_true, 'message':'User does not exist.'})
            
    
    else:
        return render(request,'default/sign_up.html')

def log_out(request):
    logout(request)
    return render (request, 'default/index.html')

@login_required
def createEvent(request):
    latitude = request.POST.get('lat')
    longitude = request.POST.get('long')
    time = request.POST.get('Time')
    icon = request.POST.get('icon')

    date_time = request.POST.get('datetimepicker')

    current_date = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())

    if not request.POST.get('datetimepicker'):
        date_time = current_date
    else:
        date_time = datetime.datetime.strptime(date_time,'%Y/%m/%d %H:%M')
        date_time = timezone.make_aware(date_time, timezone.get_default_timezone())

    str_date = str(date_time)
    str_current_date = str(current_date)

    if not request.POST.get('lat'):
        return render(request, 'default/index.html', {'message': 'Please Select Location or Timer.'})
    else:        
        if time == '30':
            title = request.POST.get('title')
            comment = request.POST.get('comment')
            current_user= request.POST.get('id')
            event = userEvent(latitude=latitude,longitude=longitude,pub_date=date_time, title=title, comments=comment,user_id=current_user, time=1800)
            event.save()
        

            my_feature = geojson.dumps(Feature(geometry=Point((float(longitude),float(latitude))), properties={"description":title, "URL": 'http://127.0.0.1:8000/event/'+str(event.id), "comment":comment, "icon": icon, "date":str_date, "current_date":str_current_date}))
            geo_obj = geojson.dumps(FeatureCollection([my_feature]))
            new_feature = geo30min(geojson_object=geo_obj, feature=my_feature,pub_date=date_time)
        
            new_feature.save()

            obj = list(geo30min.objects.values_list('feature', flat=True))
        
            feature_col = []
            for i in range(0,len(obj)):
                if obj[i]:
                    feature_col.append(geojson.loads(obj[i]))
        
            new_feature_col = geojson.dumps(FeatureCollection(feature_col))
            new_geo = geo30min(geojson_object=(new_feature_col), pub_date=date_time)
            new_geo.save()

            

            return render(request, 'default/index.html', {'message':'Event Created'})
        
    
        if time== '2':
            title = request.POST.get('title')
            comment = request.POST.get('comment')
            current_user= request.POST.get('id')
            event = userEvent(latitude=latitude,longitude=longitude,pub_date=date_time, title=title, comments=comment,user_id=current_user, time=7200)
            event.save()
        

            my_feature = geojson.dumps(Feature(geometry=Point((float(longitude),float(latitude))), properties={"description":title, "URL": 'http://127.0.0.1:8000/event/'+str(event.id), "comment":comment, "icon": icon, "date":str_date, "current_date":str_current_date}))
            geo_obj = geojson.dumps(FeatureCollection([my_feature]))
            new_feature = geo2hrs(geojson_object=geo_obj, feature=my_feature,pub_date=date_time)
        
            new_feature.save()

            obj = list(geo2hrs.objects.values_list('feature', flat=True))
        
            feature_col = []
            for i in range(0,len(obj)):
                if obj[i]:
                    feature_col.append(geojson.loads(obj[i]))
        
            new_feature_col = geojson.dumps(FeatureCollection(feature_col))
            new_geo = geo2hrs(geojson_object=(new_feature_col), pub_date=date_time)
            new_geo.save()
        
            return render(request, 'default/index.html')
        
        if time== '6':
            title = request.POST.get('title')
            comment = request.POST.get('comment')
            current_user= request.POST.get('id')
            event = userEvent(latitude=latitude,longitude=longitude,pub_date=date_time, title=title, comments=comment,user_id=current_user, time=21600)
            event.save()
        

            my_feature = geojson.dumps(Feature(geometry=Point((float(longitude),float(latitude))), properties={"description":title, "URL": 'http://127.0.0.1:8000/event/'+str(event.id), "comment":comment, "icon": icon, "date":str_date, "current_date":str_current_date}))
            geo_obj = geojson.dumps(FeatureCollection([my_feature]))
            new_feature = geo6hrs(geojson_object=geo_obj, feature=my_feature,pub_date=date_time)
        
            new_feature.save()

            obj = list(geo6hrs.objects.values_list('feature', flat=True))
        
            feature_col = []
            for i in range(0,len(obj)):
                if obj[i]:
                    feature_col.append(geojson.loads(obj[i]))
        
            new_feature_col = geojson.dumps(FeatureCollection(feature_col))
            new_geo = geo6hrs(geojson_object=(new_feature_col), pub_date=date_time)
            new_geo.save()

            return render(request, 'default/index.html')
    
    
       


def geojsondumps(request):
    #obj = list(geo.objects.values_list('feature', flat=True))
    obj_rec = geo.objects.all()

    for i in obj_rec:
        i.recent = i.was_published_recently()
        i.save()
    
    obj_recent = geo.objects.filter(recent=True)
    obj = list(obj_recent.values_list('feature',flat=True))
    
    features = []
    for i in range(0,len(obj)):
        if obj[i]:
            features.append(geojson.loads(obj[i]))
        

    #new_feature_col = geojson.dumps(FeatureCollection(features), indent=2)
    test = FeatureCollection(features)
    test = json.dumps(test)
    return render(request,'default/geojsondumps.geojson', {'api':test})



#--------------------------------------------------------------------------
def geojsondumps30min(request):

    obj_rec = geo30min.objects.all()

    for i in obj_rec:
        i.recent = i.was_published_recently()
        i.save()
    
    obj_recent = geo30min.objects.filter(recent=True)
    obj = list(obj_recent.values_list('feature',flat=True))
    
    features = []
    for i in range(0,len(obj)):
        if obj[i]:
            features.append(geojson.loads(obj[i]))
        
    test = FeatureCollection(features)
    test = json.dumps(test)
    return render(request,'default/geojsondumps30min.geojson', {'api':test})

#--------------------------------------------------------------------------
def geojsondumps2hrs(request):
    obj_rec = geo2hrs.objects.all()

    for i in obj_rec:
        i.recent = i.was_published_recently()
        i.save()
    
    obj_recent = geo2hrs.objects.filter(recent=True)
    obj = list(obj_recent.values_list('feature',flat=True))
    
    features = []
    for i in range(0,len(obj)):
        if obj[i]:
            features.append(geojson.loads(obj[i]))
        
    test = FeatureCollection(features)
    test = json.dumps(test)
    return render(request,'default/geojsondumps2hrs.geojson', {'api':test})

#--------------------------------------------------------------------------
def geojsondumps6hrs(request):
   
    obj_rec = geo6hrs.objects.all()

    for i in obj_rec:
        i.recent = i.was_published_recently()
        i.save()
    
    obj_recent = geo6hrs.objects.filter(recent=True)
    obj = list(obj_recent.values_list('feature',flat=True))
    
    features = []
    for i in range(0,len(obj)):
        if obj[i]:
            features.append(geojson.loads(obj[i]))
        
    test = FeatureCollection(features)
    test = json.dumps(test)
    return render(request,'default/geojsondumps6hrs.geojson', {'api':test})



def event(request, event_id):
    
    event_ob = get_object_or_404(userEvent, pk=event_id)
    comment = request.POST.get('comment')
    info_ob = eventInfo.objects.filter(popup_id=event_id)

    
    time_set = userEvent.objects.values_list('time', flat=True).get(pk=event_id)
    pub_date = userEvent.objects.values_list('pub_date', flat=True).get(pk=event_id)

    timer = pub_date + datetime.timedelta(seconds=time_set)

    if request.user.is_authenticated:
        if comment:
            author = request.user.username
            eventinfo_ob = eventInfo(event_comments = comment, author=author, popup_id=event_id, user_id = request.user.id)
            eventinfo_ob.save()
            eventinfo_ob = eventInfo.objects.filter(popup_id=event_id)
            return render(request, 'default/event.html', {'userEvent':event_ob, 'eventInfo':eventinfo_ob, 'Message': "Comment Created.", 'time':timer})
        else:
             return render(request, 'default/event.html', {'userEvent':event_ob, 'eventInfo':info_ob, 'Message': "Leave a comment about the event.", 'time':timer})
    else:
        return render(request, 'default/event.html', {'userEvent':event_ob, 'eventInfo':info_ob, 'Message': "Must be signed in to comment.", 'time':timer})



#------------------------------------ Private Instance --------------------------

def privateEvent(request):

    latitude = request.POST.get('lat')
    longitude = request.POST.get('long')
    icon = request.POST.get('icon')
    userid = request.POST.get('page')
    prv_obj = privateComments.objects.filter(instance=userid)
    if not request.POST.get('page'):
        return render(request, 'default/privatemap.html', {'message': 'Must be the user to post in a private instance.', 'page':userid})

    if not request.POST.get('lat'):
        return render(request, 'default/privatemap.html', {'message': 'Please Select Location or Timer.', 'page':userid})
    else:
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        user_obj = get_object_or_404(User, pk=userid)
        event = userEvent(latitude=latitude,longitude=longitude,pub_date=timezone.now(), title=title, comments=comment,user_id=userid)
        event.save()
        
        my_feature = geojson.dumps(Feature(geometry=Point((float(longitude),float(latitude))), properties={"description":title, "URL": 'http://127.0.0.1:8000/event/'+str(event.id), "comment":comment, "icon": icon}))
        geo_obj = geojson.dumps(FeatureCollection([my_feature]))
        new_feature = geoprivate(geojson_object=geo_obj, feature=my_feature,pub_date=timezone.now(), user_id = userid)
        
        new_feature.save()

        obj = list(geoprivate.objects.values_list('feature', flat=True))
        
        feature_col = []
        for i in range(0,len(obj)):
            if obj[i]:
                feature_col.append(geojson.loads(obj[i]))
        
        new_feature_col = geojson.dumps(FeatureCollection(feature_col))
        new_geo = geoprivate(geojson_object=(new_feature_col), pub_date=timezone.now(), user_id = request.user.id)
        new_geo.save()
        
        return render(request, 'default/privatemap.html', {'privateComments':prv_obj,'userEvent': event, 'page':userid })

def geojsondumpsprivate(request, userid):
    
    obj_rec = geoprivate.objects.filter(user_id = userid)

    for i in obj_rec:
        i.recent = i.was_published_recently()
        i.save()

    obj_recent = geoprivate.objects.filter(user_id=userid, recent=True)
    obj = list(obj_recent.values_list('feature',flat=True))
    
    features = []
    for i in range(0,len(obj)):
        if obj[i]:
            features.append(geojson.loads(obj[i]))
        
    test = FeatureCollection(features)
    test = json.dumps(test)
    return render(request,'default/geojsondumpsprivate.geojson', {'api':test})

    
def createPrivate(request, userid):

    prv_obj = privateComments.objects.filter(instance=userid)
    if request.user.is_authenticated:
        return render(request, 'default/privatemap.html', {'privateComments':prv_obj, 'page':userid, 'message':"Private Map Instance."})
    else:
        return render(request, 'default/index.html', {'message': "Sorry, must be signed in to create a private instance."})

def createprivatecomment(request):
    comment = request.POST.get('comment')
    page = request.POST.get('page')
    author = request.POST.get('author')
    pub_date= timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
    prv_obj = privateComments.objects.filter(instance=page)
    
    if comment:
        if author:
            new_comment = privateComments(author=author, comment=comment, pub_date=pub_date, instance=page)
            new_comment.save()
            return render(request, 'default/privatemap.html', {'privateComments':prv_obj,'comment':new_comment, 'page':page, 'message':"Comment Created"})
        else:
            new_comment = privateComments(author='Anononymous', comment=comment, pub_date=pub_date, instance=page)
            new_comment.save()
            return render(request, 'default/privatemap.html', {'privateComments':prv_obj,'comment':new_comment, 'page':page, 'message':"Comment Created"})
    else:
        return render(request, 'default/privatemap.html', {'privateComments':prv_obj,'message': "No comment entered.", 'page': page})


def about(request):
    return render(request, 'default/about.html')


def search(request):
    query = request.POST.get('query')
    event_obj = userEvent.objects.filter(title__icontains=query) | userEvent.objects.filter(comments__icontains=query)
    

    current_date = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())

    active_events_id = []
    for i in event_obj:
        if i.pub_date +  datetime.timedelta(seconds=i.time) > current_date:
            active_events_id.append(i.id)
    
    active_events = userEvent.objects.filter(id__in=active_events_id)




    return render(request, 'default/search.html',{'message':"Currently active events.", 'userEvent':active_events, 'userEvent_old': event_obj})



