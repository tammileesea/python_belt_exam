from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime 
from .models import User, Wish
import bcrypt 

def index(request):
    if "first_name" in request.session:
        return redirect("/wishes")
    return render(request, 'wish_app/index.html')

def registration_success(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else: 
        first_name = request.POST["first_name_input"]
        last_name = request.POST["last_name_input"]
        email = request.POST["email_input"]
        password = request.POST["password_input"]
        hashpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashpw)
        request.session["user_id"] = new_user.id
        request.session["first_name"] = first_name
        request.session["last_name"] = last_name
        new_user.save()
        return redirect("/wishes")

def email(request):
    email = User.objects.filter(email=request.POST["email_input"])
    context = {}
    if email:
        context = {
            "found": True,
        }
    else:
        context = {
            "found": False,
        }
    return render(request, 'wish_app/partials/email.html', context)

def login_success(request):
    users = User.objects.filter(email=request.POST["email_input"])
    if not users:
        context = {
            "login_error_message": "The email or password you entered does not match our records"
        }
        return render(request, 'wish_app/index.html', context)
    for user in users:
        if bcrypt.checkpw(request.POST["password_input"].encode(), user.password.encode()):
            request.session["user_id"] = user.id
            request.session["first_name"] = user.first_name
            request.session["last_name"] = user.last_name
            return redirect("/wishes")
        else:
            context = {
                "login_error_message": "The password you entered does not match our records"
            }
            return render(request, 'wish_app/index.html', context)

def wishes(request):
    if not "first_name" in request.session:
        return redirect("/")
    context = {
        "my_wishes": Wish.objects.filter(creator=request.session["user_id"]).exclude(granted=request.session["user_id"]),
        "granted_wishes": Wish.objects.exclude(granted=None),
        "granted_date": datetime.now(),
        "likes": len(Wish.objects.exclude(like=None))
    }
    return render(request, 'wish_app/wishes.html', context)

def log_out(request):
    try:
        del request.session["user_id"]
        del request.session["first_name"]
        del request.session["last_name"]
    except KeyError:
        return render(request, 'wish_app/wishes.html')
    return redirect('/')

def wish_page(request):
    if not "first_name" in request.session:
        return redirect("/")
    return render(request, 'wish_app/new_wish_page.html')

def create_new_wish(request):
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/new")
    else:
        item = request.POST["item_input"]
        description = request.POST["description_input"]
        creator_id = request.session["user_id"]
        new_wish = Wish.objects.create(item=item, description=description, creator_id=creator_id)
        new_wish.save()
        return redirect('/wishes')

def edit_page(request, wish_id):
    if not "first_name" in request.session:
        return redirect("/")
    context = {
        "wish_profile": Wish.objects.get(id=wish_id),
    }
    return render(request, 'wish_app/edit_page.html', context)

def edit_wish(request, wish_id):
    wish_profile = Wish.objects.get(id=wish_id)
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/wishes/edit/{wish_profile.id}")
    else:
        if request.session["user_id"] == wish_profile.creator_id:
            edited_wish = Wish.objects.get(id=wish_id)
            edited_wish.item=request.POST["item_input"]
            edited_wish.description=request.POST["description_input"]
            edited_wish.save()
            return redirect('/wishes')
        else:
            return redirect('/wishes')

def remove_wish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    if request.session["user_id"] == this_wish.creator_id:
        this_wish.delete()
        return redirect("/wishes")

def grant_wish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    if request.session["user_id"] == this_wish.creator_id:
        granted = User.objects.get(id=request.session["user_id"])
        existing_wish = Wish.objects.get(id=wish_id)
        existing_wish.granted.add(granted)
        return redirect('/wishes')

def like_wish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    if request.session["user_id"] != this_wish.creator_id:
        like = User.objects.get(id=request.session["user_id"])
        existing_wish = Wish.objects.get(id=wish_id)
        existing_wish.like.add(like)
        return redirect('/wishes')
    else:
        return redirect('/wishes')

def stats(request):
    if not "first_name" in request.session:
        return redirect("/")
    context = {
        "all_grants": len(Wish.objects.exclude(granted=None)),
        "my_grants": len(Wish.objects.filter(granted=request.session["user_id"])),
        "pending_wishes": len(Wish.objects.filter(creator=request.session["user_id"]).exclude(granted=request.session["user_id"])),
    }
    return render(request, 'wish_app/stats.html', context)