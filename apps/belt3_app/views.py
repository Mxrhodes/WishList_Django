from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from models import *

def index(request):
    #items.objects.all().delete()
    #users.objects.all().delete()
    #joins.objects.all().delete()
    #print items.objects.all()
    return render(request, "belt3_app/index.html")

def register(request):
    response = users.objects.register(
        name=request.POST["name"],
        username=request.POST["username"],
        password=request.POST["password"],
        confirm_password=request.POST["confirm_password"],
        hired=request.POST["hired"]
    )
    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'Welcome to the site!')
        request.session["user_id"] = response["user"].id
        request.session["name"] = request.POST["name"]
        request.session["username"] = request.POST["username"]
        print("user id ", request.session["user_id"])
        print(request.session["name"])

        return redirect('/dashboard')
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

        print("error here")

        return redirect("/")

def login(request):
    print request.POST
    response = users.objects.login(
        username=request.POST["username"],
        password=request.POST["password"]
    )

    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'Welcome to the site!')
        request.session["user_id"] = response["user"].id
        request.session["username"] = request.POST["username"]
        print("this is the request.session info ", request.session["username"])
        print("***   **** **** ", request.session["user_id"])
        return redirect('/dashboard')

    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
            
    return redirect("/")

def dashboard(request):
    loggedInUser = users.objects.get(id=request.session['user_id'])
    print ("the logged in user is here ", loggedInUser)

    joinedItems = joins.objects.filter(user_id=loggedInUser) 
    selectedItem = items.objects.filter(added_by=loggedInUser)
    allItems = items.objects.all().exclude(added_by=loggedInUser)

    for join in joinedItems:
        print join.item.id
        allItems = allItems.exclude(id=join.item.id)


    data = {
        'joinedItems': joinedItems,
        'selectedItem': selectedItem,
        'allItems': allItems
    }

    return render(request, "belt3_app/dashboard.html", data)

def showItem(request, item_id):

    this_item = items.objects.get(id=item_id)

    data = {
        "this_item": this_item
    }

    return render(request, "belt3_app/show.html", data)

def createItem(request):
    print "creating a new wish list item now"

    return render(request, "belt3_app/create.html")


def create(request):

    response = items.objects.validate(
        name = request.POST['name'],
        added_by = request.session['user_id']
    )
    print("----------")
    print(response)

    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'New Item has been added!')
        request.session["item_id"] = response["item"].id

        joinnedUser = users.objects.get(id=request.session['user_id'])
        createdItem = response['item']
        join_created = joins.objects.create(
            user = joinnedUser,
            item = createdItem
        )

        return redirect("/dashboard")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect('/wish_items/create')

def joinItem(request, item_id):
    #print trip_id
    joinned = joins.objects.create(
        user_id=request.session['user_id'],
        item_id=item_id
    )
    print(joinned)

    return redirect('/dashboard' )


def itemRemoved(request, item_id):
    item = joins.objects.filter(item_id=item_id)
    print("--- ", item)
    item.delete()

    return redirect("/dashboard")

def itemDelete(request, item_id):
    Item = items.objects.get(id=item_id)
    Item.delete()

    return redirect("/dashboard")

def logout(request):
    request.session.clear()

    return redirect("/")