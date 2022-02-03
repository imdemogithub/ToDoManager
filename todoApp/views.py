from django.db import connection
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from random import randint
import datetime

import pyttsx3
import os
from django.conf import settings

default_data = {
    'app_name': 'ToDo Manager',
    'form_membership': ['login_page', 'register_page', 'recovery_password_page']
}

# default page
def index(request):
    default_data['current_page'] = 'index'
    return render(request, 'index.html', default_data)

def login_page(request):
    if 'email' in request.session:
        return redirect(profile_page)

    default_data['current_page'] = 'login_page'

    engine = pyttsx3.init()
    engine.say("login page opened.")
    engine.runAndWait()
    engine.stop()
    
    return render(request, 'login_page.html', default_data)

def register_page(request):
    default_data['current_page'] = 'register_page'
    return render(request, 'register_page.html', default_data)

def recovery_password_page(request):
    default_data['current_page'] = 'recovery_password_page'
    return render(request, 'recovery_password_page.html', default_data)

def profile_page(request):
    profile_data(request)
    default_data['current_page'] = 'profile_page'
    return render(request, 'profile_page.html', default_data)

# serialize model object
def serialize_data(model_object):
    d = {}
    for k,v in model_object.__dict__.items():
        if k.startswith('_') or k.endswith('_'):
            continue
        # print('profile data: ', k)
        d.setdefault(k, v)
    return d

# profile data
def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    if profile.Avatar.url.split('/')[-1] == 'avatar.png':
        profile.Avatar = None
        profile.save()
    
    default_data['profile_data'] = serialize_data(profile)

    # print('profile data: ', profile.__dict__)

    load_connections(request)
    load_todo(request)
    # print("todo data: ", default_data['my_todo'])

    default_data['gender_choice'] = [{'short_val': i, 'text': j} for i, j in choice_gender]
    # [{'short_val': 'm', 'text': 'male'}, {'short_val': 'f', 'text': 'female'}]

    # master = Master.objects.all()
    # for m in master:
    #     print('master data: ', m.__dict__)


# profile image upload
def upload_image(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    image = request.FILES['avatar']
    
    image_name = image.name
    image_path = os.path.join(settings.MEDIA_ROOT, 'users/profile')
    images = os.listdir(image_path)

    image_extension = image_name.split('.')[-1]

    new_image_name = f"{profile.id}_{master.Email.split('@')[0]}.{image_extension}"
    image.name = new_image_name

    
    print('image name:', image_name)
    print('new name:', new_image_name)
    print('image path:', images)

    if new_image_name in images:
        os.remove(os.path.join(image_path, new_image_name))

    profile.Avatar = image

    profile.save()

    return redirect(profile_page)

# update profile data
def profile_update(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    profile.FullName = request.POST["full_name"]
    profile.Mobile = request.POST["mobile"]
    profile.Gender = request.POST["gender"]
    profile.Country = request.POST["country"]
    profile.City = request.POST["city"]
    profile.State = request.POST["state"]
    profile.Address = request.POST["address"]

    profile.save()
    

    # return redirect(profile_page)
    profile_data(request)
    default_data['msg'] = 'Profile data updated successfully.'
    return JsonResponse(default_data)

# def profile_update(request):
#     profile_data(request)
#     return JsonResponse(default_data)

# change password
def change_password(request):
    master = Master.objects.get(Email = request.session['email'])

    old_pwd = request.POST["old_password"]
    new_pwd = request.POST["new_password"]

    if master.Password == old_pwd:
        master.Password = new_pwd
        master.save()

        print("message: ", 'password changed.')
        return redirect(profile_page)
    else:
        print("message: ", 'wrong password')
        return redirect(login_page)

# register functionality
def register(request):
    print( request.POST )

    master = Master.objects.create(
        Email = request.POST['email'],
        Password = request.POST['password']
    )

    
    ref_id = f"{request.POST['email'].split('@')[0]}-{randint(1000,9999)}"
    print('ref_id: ', ref_id)
    Profile.objects.create(Master=master, RefID = ref_id)

    return redirect(register_page)

# login functionality
def login(request):
    email = request.POST['email']
    password = request.POST['password']
    
    try:
        master = Master.objects.get(Email = email)

        if master.Password == password:
            request.session['email'] = email
            return redirect(profile_page)
        else:
            print("message: ", 'wrong password')

    except Master.DoesNotExist:
        print(f"{email} is not registered.")
    
    return redirect(login_page)


# search reference
def search_ref(request):
    profile = Profile.objects.get(RefID = request.POST['ref_id'])
    
    default_data['ref_data'] = serialize_data(profile)
    default_data['msg'] = 'Reference found.'
    return JsonResponse(default_data)

# request new connection
def request_connection(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(RefID = request.POST['ref_id'])
    Connection.objects.create(Master = master, Profile = profile)

# test
def todo_craete(request):
    print("new todo data:", request.POST)

    if 'participate' in request.POST:
        participate = request.POST.getlist('participate')
    
    print('participate:', participate)
    for p in participate:
        print('participate:', p)
    return redirect(profile_page)

# new todo
def create_todo(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)
    date = request.POST['todo_deadline'].split('/')
    time = request.POST['todo_time'].split(':')

    day = int(date[1])
    month = int(date[0])
    year = int(date[2])
    hour = int(time[0])
    minutes = int(time[1])

    deadline = datetime.datetime(year, month, day, hour, minutes)

    todo = ToDo.objects.create(
        Master = master,
        Title = request.POST['todo_title'],
        Tags = request.POST['todo_tags'],
        Deadline = deadline,
        Description = request.POST['todo_description']
    )

    if 'participate' in request.POST:
        participate = request.POST.getlist('participate')

        for p in participate:
            con = Connection.objects.get(id=int(p))
            ToDoMember.objects.create(
                ToDo = todo,
                # Profile = Profile.objects.get(id=con.Profile.id)
                Profile = con.Profile
            )
    
    return redirect(profile_page)

# remove todo
def remove_todo(request, pk):
    ToDo.objects.get(id = pk).delete()

    return redirect(profile_page)

# name shortner
def shortner(obj):
    obj = obj.split()
    if len(obj) > 1:
        print("data: ", obj)
        return f"{obj[0][0]}{obj[1][0]}"
    else:
        return f"{obj[0][0]}"
        
# load connection
def load_connections(request):
    master = Master.objects.get(Email = request.session['email'])
    connections = Connection.objects.filter(Master = master)

    for c in connections:
        # print('data: ', c.Profile.FullName)
        c.Profile.SortName = shortner(c.Profile.FullName)
        # print('c profile', c.Profile)
        if c.Profile.Avatar.url.split('/')[-1] == 'avatar.png':
            c.Profile.Avatar = None
            c.Profile.save()

    default_data['my_connection'] = connections
    
# load todo and members
def load_members(request):
    master = Master.objects.get(Email = request.session['email'])
    todo = ToDo.objects.get(Master = master)
    todo_members = ToDoMember.objects.filter(ToDo = todo)
    default_data['todo_members'] = todo_members

def load_todo(request):
    master = Master.objects.get(Email = request.session['email'])
    my_todo = ToDo.objects.filter(Master = master)
    
    default_data['my_todo'] = []

    for i in my_todo:
        i.Date = i.Deadline.strftime("%m/%d/%Y")
        i.Time = i.Deadline.strftime("%X")[:-3]
        # print(i.Date)
        # print('todo member:', ToDoMember.objects.filter(ToDo = i))
        # print('todo', i)
        
        members = ToDoMember.objects.filter(ToDo = i)
        for m in members:
            m.Profile.SortName = shortner(m.Profile.FullName)

        default_data['my_todo'].append({
            'todo': i,
            'members': members,
        })

    # print(default_data['my_todo'])
    # print('reversed', my_todo[::-1])
    default_data['my_todo'] = default_data['my_todo'][::-1]

# add connection
def add_connection(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    connection = Connection.objects.get(Profile=profile)
    connection.Status = 'active'

# sign out
def sign_out(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(login_page)