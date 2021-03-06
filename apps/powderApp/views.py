from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . import models
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

###################### Login and Registration Section

def index(request):
    if not 'active_user' in request.session:
        request.session['active_user'] = ""
    return render(request, 'powderApp/index.html')

def success(request):
    if request.session['active_user'] == "" or not 'active_user' in request.session:
        messages.add_message(request, messages.ERROR, "Please Login to Continue")
        return redirect('/')
    else:
        # some query to pull up the user's run history

        # context = {
        #     send through the results of the query here
        # }
        return render(request, 'powderApp/success.html')

def python_add_user(request):
    result = models.User.objects.register(request.POST)
    if result[0] == False:
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        return log_user_in(request, result[1])

@csrf_exempt
def login(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    result = models.User.objects.login(body_data)
    if result[0] == False:
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        return log_user_in(request, result[1])

def log_user_in(request, user):
    request.session['active_user'] = {
        'id' : user.id,
        'username' : user.username,
        'email' : user.email,
    }
    return redirect ('/success')

def logout(request):
    del request.session['active_user']
    return redirect('/')

# ---------- End of Login and Registration Section -------

##### httpresponse route to process GET requests for runData ---------
@csrf_exempt
def tasks(request):
    if request.method == "GET":
        allUsers = models.User.objects.all()
        response = serializers.serialize('json', allUsers)
        return HttpResponse(response)
    elif request.method == "POST":

        new_powder_run = models.PowderRun.objects.add_new_powder_run(request.body)
        return HttpResponse(new_powder_run)

@csrf_exempt
def add_user(request):
    print("made it in to route")
    if request.method == "POST":
        print('making it to route through post')
        print(request.body)
        # body_unicode = request.body.decode('utf-8')
        print("able to set body_unicode")
        # body_data = json.loads(request.body)
        print("able to set body_Data")
        result = models.User.objects.register(request.body)
        if result[0] == False:
            print('could not create user')
            for i in result[1]:
                messages.add_message(request, messages.ERROR, i)
            print("In add_user, made it to for loop when result0 is false")
            response = serializers.serialize('json', result[1])
            return HttpResponse(response)
        else:
            print('can create user')
            print(result[1].username)
            print(result[1].id)
            print(result[1])
            query = models.User.objects.get(id= result[1].id)
            response = serializers.serialize('json', query)
            return HttpResponse(response)        # log_user_in(request, result[1])
    return HttpResponse("hello world")
