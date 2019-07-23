from __future__ import unicode_literals
from django.db import models


class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors = {}
        if len(postData['FirstName']) <= 2:
            errors["FirstName"] = "Firstname should at least 2 characters" 
      
        if len(postData['LastName']) <= 2:
            errors["LastName"] = "Lastname should at least 2 characters" 
        
        if len(postData['email']) < 10:
            errors["email"] = "email should be at least 10 characters"
        
        if len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters"
        
        if postData['password'] != postData['confirmpassword']:
            errors["checkpassword"] = "password do not match"

        return errors

        

    def login_validator(self, postData):
        errors = {}
        errors["checklogin"] = "Please enter correct email and password"
        # if len(postData['password']) < 8:
        #     errors["password"] = "password should be at least 8 characters"
        return errors


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CreattripManager(models.Manager):
    def create_new_trip_validator(self,postData):
        errors = {}
        if len(postData["destination"]) <= 3:
            errors["destination"] = "destination should at least 3 characters" 
        if len(postData["startdate"]) <= 1:
            errors["startdate"] = "startdate must be provided" 
        if len(postData["enddate"]) <= 1:
            errors["enddate"] = "enddate must be provided" 
        if len(postData["plan"]) <= 3:
            errors["plan"] = "plan should at least 3 characters" 

        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="user_job")
    plan = models.CharField(max_length=255)
    objects = CreattripManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    