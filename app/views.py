from ast import Mod
import json
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Prof, Rating, Module, User

# Create your views here.

@csrf_exempt
def Login(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'POST'):
        bad.content = "POST only"
        return bad
    un = request.POST['username']
    pw = request.POST['password']
    data = "username = " + un + ", password = " + pw
    user = authenticate(request, username=un, password=pw)
    if user is not None:
        if user.is_active:
            login(request, user)
            if(user.is_authenticated):
                print(user.username + " is logged in")
            return HttpResponse("logged in")
        else:
            return HttpResponse("disabled account")
    else:
        return HttpResponse("invalid login" + data)

@csrf_exempt
def Register(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'POST'):
        bad.content = "POST only"
        return bad
    un = request.POST['username']
    pw = request.POST['password']
    em = request.POST['email']
    data = "username = " + un + ", password = " + pw + ", email = " + em
    user = User.objects.create_user(username=un, email=em, password=pw)
    if user is not None:
        if user.is_active:
            login(request, user)
            if(user.is_authenticated):
                print(user.username + " is logged in")
            return HttpResponse("registered")
        else:
            return HttpResponse("disabled account")
    else:
        return HttpResponse("invalid registration" + data)

@csrf_exempt
def Logout(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'POST'):
        bad.content = "POST only"
        return bad
    logout(request)
    good = HttpResponse("logged out")
    good.status_code = 200
    good.reason_phrase = "OK"
    return good

def List(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'GET'):
        bad.content = "GET only"
        return bad
    modules = Module.objects.all().values("pk","title","year","semester","modID")
    return_list = []
    for record in modules:
        item = {"title":record["title"],"year":record["year"],"semester":record["semester"],"modID":record["modID"]}
        modItem = Module.objects.get(pk=record["pk"])
        profList = []
        for prof in modItem.profs.all():
            profList.append(str(prof))
        item["profs"] = profList
        return_list.append(item)
    payload = {"module_list": return_list}
    good = HttpResponse(json.dumps(payload))
    good["Content-Type"] = "application/json"
    good.status_code = 200
    good.reason_phrase = "OK"
    return good

def View(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'GET'):
        bad.content = "GET only"
        return bad
    ratings = Rating.objects.all()
    return_list = {}
    for record in ratings:
        if record.prof.name in return_list:
            return_list[record.prof.name][0] += record.val
            return_list[record.prof.name][1] += 1
        else:
            return_list[record.prof.name] = [record.val,1]
    for k, v in return_list.items():
        return_list[k] = round(v[0]/v[1])
    payload = {"rating_list": return_list}
    good = HttpResponse(json.dumps(payload))
    good["Content-Type"] = "application/json"
    good.status_code = 200
    good.reason_phrase = "OK"
    return good

@csrf_exempt
def Average(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'POST'):
        bad.content = "POST only"
        return bad
    modID = request.POST["moduleID"]
    profID = request.POST["profID"]
    ratings = Rating.objects.all().filter(module__modID=modID, prof__profID=profID)
    return_list = {}
    for record in ratings:
        if record.prof.name in return_list:
            return_list[record.prof.name][0] += record.val
            return_list[record.prof.name][1] += 1
        else:
            return_list[record.prof.name] = [record.val,1]
    for k, v in return_list.items():
        return_list[k] = round(v[0]/v[1])
    payload = {"rating_list": return_list}
    good = HttpResponse(json.dumps(payload))
    good["Content-Type"] = "application/json"
    good.status_code = 200
    good.reason_phrase = "OK"
    return good

@csrf_exempt
def Rate(request):
    bad = HttpResponseBadRequest()
    if(request.method != 'POST'):
        bad.content = "POST only"
        return bad
    modID = request.POST["moduleID"]
    profID = request.POST["profID"]
    year = request.POST["year"]
    semester = request.POST["semester"]
    try:
        rating = int(request.POST["rating"])
    except ValueError:
        bad.content = "rating must be an integer"
        return bad
    if rating < 1 or rating > 5:
        bad.content = "rating must be 1-5"
        return bad
    if not request.user.is_authenticated:
        bad.content = "Must be logged in"
        return bad
    modules = Module.objects.all().filter(modID=modID, year=year, semester=semester)
    if modules.count() == 0:
        bad.content = "No module found"
        return bad
    profs = modules[0].profs.all().filter(profID=profID)
    if profs.count() == 0:
        bad.content = "Professor doesn't teach that module"
        return bad
    existing = Rating.objects.all().filter(user=request.user, prof=profs[0], module=modules[0])
    if existing.count() != 0:
        bad.content = "You have already rated this professor for this module"
        return bad
    r = Rating(user=request.user, val=rating, prof=profs[0], module=modules[0])
    r.save()
    good = HttpResponse("rated")
    good.status_code = 200
    good.reason_phrase = "OK"
    return good