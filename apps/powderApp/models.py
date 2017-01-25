from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+')

class UserManager(models.Manager):
    def login(self, post):
        login_email = post['login_email']
        login_password = post['login_password']

        errors =[]

        user_list = User.objects.filter(email = login_email)

        if len(login_email) < 1:
            errors.append('Email is required')
        if len(login_password) < 1:
            errors.append('Password is required')
        if user_list:
            active_user = user_list[0]
            password = login_password.encode()
            if bcrypt.hashpw(password, active_user.pw_hash.encode()) == user_list[0].pw_hash :
                return (True, active_user)
            else:
                errors.append('Email and password do not match')
        else:
            errors.append('Email does not exist')
        return (False, errors)

    def register(self, post):
        username = post['username']
        email = post['email']
        password = post['password']
        confirm_password = post['confirm_password']

        errors = []
        user_list = User.objects.filter(email = email)
        # alias_list = User.objects.filter(alias = alias)
        if len(username) < 1:
            errors.append('Userame is required')
        if len(username) < 3:
            errors.append('Username requires more than 2 characters')
        if not name_regex.match(username):
            errors.append('username must only contain letters')
        # if len(alias) < 1:
        #     errors.append('Alias is required')
        # if len(alias) < 3:
        #     errors.append('Alias requires more than 2 characters')
        # if alias_list:
        #     errors.append('Alias already exists')
        if not EMAIL_REGEX.match(email):
            errors.append('Email is invalid!')
        if user_list:
            errors.append('Email already exists!')
        if len(password) < 1:
            errors.append('Password is required')
        if len(password) < 8:
            errors.append('Password should be at least 8 characters')
        if password != confirm_password:
            errors.append('Passwords do not match!')
        if len(errors) > 0:
            return (False, errors)
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = self.create(username=username, email=email, pw_hash=pw_hash)
        return (True, user)


class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class PowderRunManager(models.Manager):
    #add in other fields that will be passed through and saved to each powderRun
    def add_new_powder_run(self, post):
        altitudeDrop = post['altitudeDrop']
        distance = post['distance']
        time = post['time']
        topSpeed = post['topSpeed']
        avgSpeed = post['avgSpeed']
        biffsCount = post['biffsCount']
        jumpsCount = post['jumpsCount']
        userID = post['userID']
        user = User.objects.get(id=userID)
        new_powder_run = self.create(user=user, altitudeDrop=altitudeDrop, distance=distance, time=time, topSpeed=topSpeed, avgSpeed=avgSpeed, biffsCount=biffsCount, jumpsCount=jumpsCount)
        return (True, new_powder_run)

    def delete_powder_run(self, post):
        runID = post['powderrun_id']
        ##### identify the correct run by run_id
        # runToBeDeleted = PowderRun.objects.get(id=runID)
        deletedRun = self.delete(id=runID)
        return (True, deletedRun)


class PowderRun(models.Model):
    user = models.ForeignKey(User)
    altitudeDrop = models.CharField(max_length=5)
    distance = models.CharField(max_length=5)
    time = models.CharField(max_length=5)
    topSpeed = models.CharField(max_length=5)
    avgSpeed = models.CharField(max_length=5)
    biffsCount = models.CharField(max_length=5)
    jumpsCount = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
