from django.shortcuts import render,redirect
from django.db.models import Q
from .models import User,BloodRequest

from django.core.files.storage import FileSystemStorage

def uploadpic(request):
    mypic = request.FILES.get('mypic')

    fs = FileSystemStorage("BloodBank/static/assets/user")
    file = fs.save(mypic.name, mypic)
    fileurl = fs.url(file)
    id = request.session['loginuser']['userid']
    user = User.objects.get(pk=id)
    user.profilepic = fileurl
    user.save()
    data = request.session['loginuser']
    data['profilepic'] = fileurl
    request.session['loginuser'] = data
    return redirect('/user/home')

def changepassword(request):
    oldpwd = request.POST.get('oldpassword')
    newpwd = request.POST.get('newpassword')
    id = request.session['loginuser']['userid']
    user = User.objects.get(pk=id)

    if user.password==oldpwd:
        user.password = newpwd
        user.save()
        return redirect("/user/logout")
    else:
        request.session['passwordstatus'] = False 
        return redirect('/user/profile')        

def profile(request):
    msg = ""       
    if 'passwordstatus' in request.session:
        msg = "Old Password Not Match !" 
        del request.session['passwordstatus']
    return render(request,'profile.html',{
        'msg' : msg
    })

def saverequest(request):
    id = request.session['loginuser']['userid']
    user = User.objects.get(pk=id)

    ob = BloodRequest()
    ob.name = request.POST.get('name')
    ob.bloodgroup = request.POST.get('group')
    ob.phone = request.POST.get('phone')
    ob.hospital = request.POST.get('hospital')
    ob.city = request.POST.get('city')
    ob.requestby = user
    ob.save()
    return redirect('/user/request')

def bloodrequest(request):
    id = request.session['loginuser']['userid']
    user = User.objects.get(pk=id)

    myreq = BloodRequest.objects.filter(Q(requestby=user))
    otherreq = BloodRequest.objects.filter(~Q(requestby=user))

    return render(request,'request.html',{
        'myreq' : myreq,
        'otherreq' : otherreq
    })

def home(request):
    print(request.session['loginuser'])
    name = request.session['loginuser']['name']
    id = request.session['loginuser']['userid']

    users = User.objects.filter(~Q(id=id) & Q(isverify=True))

    return render(request,'userhome.html',{
        'name' : name , 'users' : users
    })
def logout(request):
    del request.session['loginuser']
    return redirect("/login")


