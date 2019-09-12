from django.urls import path, include
from django.conf.urls import url
from . views import *
urlpatterns = [
    #path('', Home, name='Home'),
    path('', Login, name='Login'),
    path('profile/', Profile, name='Profile'),
    path('register/', Register, name='Register'),
    path('feed/', Feed, name="Feed"),
    path('friends/', Friends, name="Friends"),
    path('addfriend/', Add_Friend, name="Add_Friend"),
    url(r'View_Profile/$', View_Profile),
    url(r'addfriend/View_Profile/$', View_Profile),
    path('editprofile/', Edit_Profile, name="Edit_Profile"),
    url(r'addfriend/FriendRequest/$', FriendRequest),
    path('search/', Search, name="Search"),
    path('upload/', Upload, name="Upload"),
    url(r'friends/Remove/$', Remove),
    path('notification/', Notification, name="Notification"),
    url(r'notification/Add/$', Add),
    url(r'notification/Reject/$', Reject),
    url(r'Logout/', Logout),
]