from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . import models
from django.core import serializers


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

def login(request):
    result = models.User.objects.login(request.POST)
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
def tasks(request):
    if request.method == "GET":
        allUsers = models.User.objects.all()
        response = serializers.serialize('json', allUsers)
        return HttpResponse(response)
    elif request.method == "POST":
        new_powder_run = models.PowderRun.objects.add_new_powder_run(request.POST)
        return HttpResponse(new_powder_run)


def add_user(request):
    result = models.User.objects.register(request.POST)
    if result[0] == False:
        for i in result[1]:
            messages.add_message(request, messages.ERROR, i)
        return redirect('/')
    else:
        response = serializers.serialize('json', result[1])
        return HttpResponse(response)
        # log_user_in(request, result[1])
