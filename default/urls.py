from django.urls import path
from . import views

app_name = 'default'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.sign_up, name = 'sign_up'),
    path('acc_created', views.acc_created, name = 'acc_created'),
    path('user', views.logged_in, name = 'logged_in'),
    path('logged_out', views.log_out, name='log_out'),
    path('createEvent', views.createEvent, name='createEvent'),
    path('geojsondumps.geojson', views.geojsondumps, name='geojsondumps'),

    path('geojsondumps30min.geojson', views.geojsondumps30min, name='geojsondumps30min'),
    path('geojsondumps2hrs.geojson', views.geojsondumps2hrs, name='geojsondumps2hrs'),
    path('geojsondumps6hrs.geojson', views.geojsondumps6hrs, name='geojsondumps6hrs'),
    
    path('geojsondumpsprivate.geojson/<int:userid>', views.geojsondumpsprivate, name='geojsondumpsprivate'),
    path('privatemap/<int:userid>', views.createPrivate, name='createPrivate'),
    path('privatemap/privateEvent', views.privateEvent, name='privateEvent'),
    path('privatemap/createprivatecomment', views.createprivatecomment, name='createprivatecomment'),

    path('about', views.about, name='about'),


    path('event/<int:event_id>', views.event, name='event'),
    path('event/search', views.search, name='search'),
]