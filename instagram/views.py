from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from . models import *
from django.contrib import messages
from django.http import HttpResponse

def Home(request):
    return render(request, 'home.html', None)
def Login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            a = user.objects.get(username=username)
        except user.DoesNotExist:
            messages.error(request, 'Invalid user!?')
            return redirect('Login')
        if a.password != password:
            messages.error(request, 'Incorrect password!?')
            return redirect('Login')
        request.session['username'] = username
        request.session['id'] = a.id
        return redirect('Feed')
    return render(request, "login.html", None)
def Logout(request):
    request.session['username'] = None
    request.session['id'] = None
    return redirect('Login')

def Register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        q = user.objects.all()
        if username in [u.username for u in q]:
            messages.error(request, "username already taken!?")
            return redirect('Register')
        if email in [e.email for e in q]:
            messages.error(request, "Email already exists!?")
            return redirect('Register')
        if phone in [p.phone for p in q]:
            messages.error(request, "Number already exists!?")
            return redirect('Register')
        if password1 != password:
            messages.error(request, "Pw doesn't match")
            return redirect('Register')
        try:
            img = request.FILES['image']
            a = user(username=username, email=email, phone=phone, dob=dob, password=password, image=img)
        except MultiValueDictKeyError:
            a = user(username=username, email=email, phone=phone, dob=dob, password=password)
        a.save()
        messages.success(request, "Registered! Now Login to Your account...")
        return redirect('Login')
    return render(request, 'register.html', None)
def Feed(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    id = request.session.get('id')
    f = friendlist.objects.filter(userid=id)
    fr = [user.objects.get(username=i.friends).id for i in f]
    fr.append(id)
    b = [post.objects.filter(userid=j) for j in fr if post.objects.filter(userid=j).exists()]
    return render(request, 'feed.html', {'b': b})
def Profile(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    username = request.session.get('username')
    a = user.objects.get(username=username)
    if post.objects.filter(userid=a.id).exists():
        b = post.objects.filter(userid=a.id)
    else:
        b = None
    return render(request, 'profile.html', {'a': a, 'b': b})
def View_Profile(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    username = request.GET.get('friend')
    a = user.objects.get(username=username)
    if post.objects.filter(userid=a.id).exists():
        b = post.objects.filter(userid=a.id)
    else:
        b = None
    return render(request, 'viewprofile.html', {'a': a, 'b': b})
def Edit_Profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        u = request.session.get('username')
        q = user.objects.exclude(username=u)
        if username in [u.username for u in q]:
            messages.error(request, "username already taken!?")
            return redirect('Edit_Profile')
        if email in [e.email for e in q]:
            messages.error(request, "Email already exists!?")
            return redirect('Edit_Profile')
        if phone in [p.phone for p in q]:
            messages.error(request, "Number already exists!?")
            return redirect('Edit_Profile')
        if password1 != password:
            messages.error(request, "Pw doesn't match")
            return redirect('Edit_Profile')
        a = user.objects.get(username=u)
        a.username = username; a.email = email; a.phone = phone; a.dob = dob; a.password = password
        try:
            img = request.FILES['image']
            a.image = img
        except MultiValueDictKeyError:
            pass
        a.save()
        return redirect('Profile')
    id = request.session.get('id')
    a = user.objects.get(id=id)
    return render(request, 'editprofile.html', {'a': a})

def Friends(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    id = request.session.get('id')
    if friendlist.objects.filter(userid=id).exists():
        a = friendlist.objects.filter(userid=id)
        temp = {i.friends: user.objects.get(username=i.friends).image for i in a}
        return render(request, 'friends.html', {'fr': temp})
    return render(request, 'friends.html', None)
def Remove(request):
    id = request.session.get('id')
    friend = request.GET.get('friend')
    friendlist.objects.filter(userid=id, friends=friend).delete()
    return redirect('Friends')
def Add_Friend(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    id = request.session.get('id')
    username = request.session.get('username')
    a = user.objects.exclude(id=id)
    if friendlist.objects.filter(userid=id).exists():
        b = friendlist.objects.filter(userid=id).values_list('friends', flat=True)
        fr = [i for i in b]
        if notifications.objects.filter(friendrequest=username).exists():
            c = notifications.objects.filter(friendrequest=username)
            frqst = [i.userid.username for i in c]
        else:
            frqst = []
        temp = {i.username: i.image for i in a if i.username not in fr and i.username not in frqst}
        return render(request, 'addfriend.html', {'temp': temp})
    temp = {i.username: i.image for i in a}
    return render(request, 'addfriend.html', {'temp': temp})
def FriendRequest(request):
    friend = request.GET.get('friend')
    frnd = user.objects.get(username=friend)
    username = request.session.get('username')
    userid = user.objects.get(username=username)
    friendlist(userid=userid, friends=friend).save()
    notifications(userid=frnd, label='friendrequest', friendrequest=username, info=None).save()
    return redirect('Add_Friend')
def Add(request):
    id = request.session.get('id')
    friend = request.GET.get('friend')
    u = user.objects.get(id=id)
    a = friendlist(userid=u, friends=friend)
    a.save()
    userid = user.objects.get(username=friend)
    b = notifications(userid=userid, label='info', info=u.username)
    b.save()
    notifications.objects.filter(userid=id, friendrequest=friend).delete()
    return redirect('Notification')
def Reject(request):
    id = request.session.get('id')
    friend = request.GET.get('friend')
    notifications.objects.filter(userid=id, friendrequest=friend).delete()
    return redirect('Notification')
def Search(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    if request.method == "POST":
        username = request.POST.get('username')
        if user.objects.filter(username=username).exists():
            a = user.objects.get(username=username)
            if post.objects.filter(userid=a.id).exists():
                b = post.objects.filter(userid=a.id)
            else:
                b = None
            return render(request, 'viewprofile.html', {'a': a, 'b': b})
        messages.error(request, "User doesn't exists!?")
        return redirect('Search')
    return render(request, 'Search.html', None)
def Upload(request):
    if request.method == "POST":
        img = request.FILES['image1']
        id = request.session.get('id')
        u = user.objects.get(id=id)
        a = post(userid=u, posts=img)
        a.save()
        return redirect('Feed')
    return render(request, 'upload.html', None)
def Notification(request):
    if request.session.get('id') is None:
        messages.error(request, "Session expired! Login again..")
        return redirect('Login')
    id = request.session.get('id')
    if notifications.objects.filter(userid=id).exists():
        a = notifications.objects.filter(userid=id)
        reqst = [i.friendrequest for i in a if i.friendrequest]
        inf = [i.info for i in a if i.info]
    else:
        reqst = []
        inf = []
    return render(request, 'notification.html', {'reqst': reqst, 'inf': inf})