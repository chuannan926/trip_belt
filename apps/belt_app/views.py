from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, 'belt_app/index.html')


def process_reg(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print("Registration validation failed!")
        return redirect("/")
    else: #  We do not have error,start register new user!
        hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        print(f"************* hash1 = {hash1}")
       
        
        created_user = User.objects.create(firstname=request.POST["FirstName"],lastname=request.POST["LastName"],email=request.POST["email"],password=hash1)
        # THIS LOGS IN THE USER
        request.session["logged_in_user_id"] = created_user.id
        request.session["FirstName"] = created_user.firstname
        return redirect("/dashboard")

def process_log(request):
    # Run the login validator
    # errors = User.objects.login_validator(request.POST)

    # # If there are validation errors
    # if len(errors) > 0:
    #     # Then kick them back to login page with validation errors
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect("/")

    # # If there are NO validation errors
    # else: 
    try:
        # Find a list of all the users that match this email
        list_of_logging_in_user = User.objects.filter(email=request.POST["email"]).all()

        # If there is user that matches that email
        if len(list_of_logging_in_user) > 0:

            logging_in_user = list_of_logging_in_user[0]

            # If their password matches the hashed password in the DB
            if bcrypt.checkpw(request.POST["password"].encode(), logging_in_user.password.encode()):
                # Log in the user and go to success
                request.session["logged_in_user_id"] = logging_in_user.id
                request.session["FirstName"] = list_of_logging_in_user[0].firstname

                return redirect("/dashboard")
            # If their password DOESN'T match the hashed pass in the DB
            else:
                errors = User.objects.login_validator(request.POST)
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                # Then kick them back to the login page
                return redirect("/")

        # If there is NO user that matches that email
        else:
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            return redirect("/")
    except:
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        return redirect("/")

    
        

 

def dashboard(request):
    if "logged_in_user_id" not in request.session:
        return redirect("/")

    else:
        user=User.objects.get(id=request.session["logged_in_user_id"])
        print (user.firstname)
        context ={
        "registered_user":user,
        "all_trips":Trip.objects.all(),
       
        }
   
        return render(request, 'belt_app/dashboard.html',context)


def logout(request):
    request.session.clear()
    return redirect("/")


def new(request):
    return render(request,'belt_app/new.html')


def process_new_trip(request):
    print("Request.POST *************************")
    print(request.POST["destination"])
    errors = Trip.objects.create_new_trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
# if validator check there is sth wrong, return same page.
    else:
        trip_creator=User.objects.get(id=request.session["logged_in_user_id"])
        print(request.POST)
        created_trip = Trip.objects.create(destination=request.POST["destination"],startdate=request.POST["startdate"],enddate=request.POST["enddate"],plan=request.POST["plan"],creator=trip_creator)
    
        return redirect("/dashboard")

def view_trip(request,trip_id):
    print(trip_id)

    context = {
        "selected_trip": Trip.objects.get(id = trip_id), 
    }
    return render(request,'belt_app/view.html',context)

def remove_trip(request,trip_id):
 
    trip_to_remove=Trip.objects.get(id=trip_id)
    if request.session["logged_in_user_id"] == trip_to_remove.creator.id:
        trip_to_remove.delete()
    return redirect("/dashboard")

def view_edit_trip(request,trip_id):
   
    context ={
        "trip_info_id":Trip.objects.get(id=trip_id),
    }
    return render(request,'belt_app/edit.html',context)

def process_edit_trip(request,trip_id):
    print("Request.POST *************************")
    print(request.POST["destination"])

    errors = Trip.objects.create_new_trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit/' + trip_id)

    else :
        trip_to_edit=Trip.objects.get(id=trip_id)
        print(request.POST)
        trip_to_edit.destination = request.POST["destination"]
        trip_to_edit.startdate = request.POST["startdate"]
        trip_to_edit.enddate = request.POST["enddate"]
        trip_to_edit.plan = request.POST["plan"]
        trip_to_edit.save()

        return redirect("/dashboard")