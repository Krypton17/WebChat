import json,requests
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from main.models import User


def homepage(request):
    if User.name != None:
        return redirect('main:room',room_name='chat')
    return redirect('main:login')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'rooms':User.rooms,
        'username': mark_safe(json.dumps(User.name))
    })


# will send to registration page or registration request to server
def register(request):
    if request.method == "POST":
        # send registration request to server
        register_request(register_data(request))
    # send back to registration page
    return render(request,'registration.htm')


def login(request):
    # login button action
    if request.method == "POST":
        # json that will be send to server for login procedure
        return login_request(request)
    return render(request,'login_page.htm')


def register_request(json):
    try:
        r = requests.post('http://localhost:3000/register', json)
        # API response
        if r.text != "Registration success":
            render(request,'registration.htm')
        else:
            return login_request(request)
    except Exception as e:
        print(e)


def login_request(request):
    # send login request to server
    try:
        r = requests.post('http://localhost:3000/login', login_data(request))
        # API response
        response = r.json()
        response_message = response['message']
        User.name = response['name']
        for room in response['rooms']:
            User.rooms.append(room)
        if response_message == "Login success":
            return redirect('main:room',room_name='chat')
        else:
            return login(request)
    except Exception as e:
        print(e)

# data for request POST
def register_data(request):
    return {
        "email": str(request.POST.get('email')),
        "name": str(request.POST.get('username')),
        "password": str(request.POST.get('password'))
    }


def login_data(request):
    return {
        "email": str(request.POST.get('email')),
        "password": str(request.POST.get('password'))
    }
