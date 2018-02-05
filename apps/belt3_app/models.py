from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime

PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')


class usersManager(models.Manager):
    def register(self, name, username, password, confirm_password, hired):

        now = datetime.now()

        response = {
            "errors": [],
            "valid": True,
            "user": None
        }

        if len(name) < 3:
            response["valid"] = False
            response["errors"].append("Name is to short, please provide a Fullname")
            print(1)
        if now < datetime.strptime(hired, "%Y-%m-%d"):
            response["valid"] = False
            response["errors"].append("Hired date must be in the past")
            print(2)
        if len(username) < 3:
            response["valid"] = False
            response["errors"].append("Username is required")
            print(3)
        else:
            list_of_username = users.objects.filter(username=username.lower())
            if len(list_of_username) > 0:
                response["valid"] = False
                response["errors"].append("Username already exists")
            print(4)
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be 8 characters or more with uppercase letter(s) and number(s)")
        elif not PASSWORD_REGEX.match(password):
            response["valid"] = False
            response["errors"].append("Invalid password. Password must contain at least one uppercase letter and at least one number")
            print(5)
        if confirm_password != password:
            response["valid"] = False
            response["errors"].append("Password must match Confirm Password")
            print(6)

        if response["valid"]:
            response["user"] = users.objects.create(
                name=name,
                username=username,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
                hired=hired
            )

        return response

    def login(self, username, password):

        response = {
            "errors": [],
            "valid": True,
            "user": None
        }

        if len(username) < 3:
            response["valid"] = False
            response["errors"].append("Username is required")
        else:
            print "***",username
            list_of_username = users.objects.filter(username=username.lower())
            print(list_of_username)
            if len(list_of_username) == 0:
                #meaning not there
                response["valid"] = False
                print("something is here ", list_of_username)
                response["errors"].append("Username does not exist")
            else:
                print("something is here ", list_of_username)
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be 8 characters or more")
        elif not PASSWORD_REGEX.match(password):
            response["valid"] = False
            response["errors"].append("Invalid password. Password must contain at least one uppercase letter and at least one number")

        if response["valid"]:
            if bcrypt.checkpw(password.encode(), list_of_username[0].password.encode()):
                response["user"] = list_of_username[0]
                
            else:
                response["valid"] = False
                response["errors"].append("Incorrect Password")

        return response

class itemsManager(models.Manager):
    def validate(self, name, added_by):
        response = {
            "errors": [],
            "valid": True,
            "item": None
        }

        if len(name) < 4:
            response["valid"] = False
            response["errors"].append("Item/Product is required")

        addedByObject = users.objects.get(id=added_by)

        print("addedByObject = ", addedByObject)

        if response["valid"]:
            response["item"] = items.objects.create(
                name=name,
                added_by=addedByObject
            )
        print "=================="
        print response["valid"]
        print added_by

        return response

class users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    hired = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = usersManager()

class items(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added_by = models.ForeignKey(users, related_name="adder")

    objects = itemsManager()

class joins(models.Model):
    user = models.ForeignKey(users, related_name="joined_items") 
    item = models.ForeignKey(items, related_name="joined_users") 
