from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
import requests,json,time

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('supermanager_page')
                    elif user.is_student:
                        return redirect('student_dash')
                    else:
                        return redirect('courses_page')
            else:
                messages.error(request, 'Wrong password')
        else:
            messages.error(request, 'Username doesn"t exist')

    return render(request, 'index.html')

def logout_page(request):
    logout(request)
    return redirect('homepage')



zoom_client_id = "jLHVm_eYQlSkK1C2vqvrkw"
zoom_client_secret = "ssULJTQxfkEm8GXuQpuMfxQxeMq4iik4"
redirect_uri = "http://127.0.0.1:8000/zoom_auth"

def zoom(request):
    authorization_url = "https://zoom.us/oauth/authorize"
    auth_params = {
        "response_type": "code",
        "client_id": zoom_client_id,
        "redirect_uri": redirect_uri
    }
    auth_url = authorization_url + "?" + "&".join(f"{key}={value}" for key, value in auth_params.items())
    print(f"Please authorize the application by visiting the following URL:\n{auth_url}")
    return redirect(auth_url)
    context = {
    }
    return render(request, 'zoom.html',context)

from .models import Teacher
from Scheme.models import Meeting
from Course.models import Course

import jwt,random,datetime

def key_is_present(dictionary, key):
    return key in dictionary

def zoom_auth(request):
    token_url = "https://zoom.us/oauth/token"
    authorization_code = request.GET.get('code') 

    token_params = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": zoom_client_id,
        "client_secret": zoom_client_secret,
        "redirect_uri": redirect_uri
    }

    teacher = Teacher.objects.get(name=request.user)
    data = requests.post(token_url, data=token_params).json()
    if key_is_present(data,'access_token'):
        teacher.access_token = data["access_token"]
        teacher.save()

    expiration_time = jwt.decode(teacher.access_token, algorithms=["HS256"], options={"verify_signature": False})['exp']
    current_time = time.time()
    token_is_expired = current_time > expiration_time
    
    url = "https://api.zoom.us/v2/users/me/meetings"

    if token_is_expired:
        return redirect('zoom_page')
    else:
        if request.method == 'POST':
            topic = request.POST.get('topic')
            start_date = request.POST.get('start_date')
            start_time = request.POST.get('start_time')
            duration = request.POST.get('duration')
            course = request.POST.get('course')

            if Meeting.objects.filter(course=Course.objects.get(slug=course)).count() > 2:
                messages.error(request,'Course Maximum Reached')
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {teacher.access_token}"
                }

                day_count = datetime.datetime.strptime(f'{start_date+"T"+start_time+":00"+"Z"}', '%Y-%m-%dT%H:%M:%SZ').weekday()
                pass_code = random.randint(100000,999999)
                payload = {
                    "topic": topic,
                    "type": 2,
                    "start_time": f'{start_date+"T"+start_time+":00"+"Z"}',
                    "duration": duration,
                    "timezone": "GMT",
                    "password": pass_code,
                    "agenda": course,
                    "pre_schedule": False,
                    "recurrence": {
                        "end_date_time": "2022-04-02T15:59:00Z",
                        "end_times": 7,
                        "monthly_day": 1,
                        "monthly_week": 1,
                        "monthly_week_day": 1,
                        "repeat_interval": 1,
                        "type": 1,
                        "weekly_days": "1"
                    },
                }
            
                response = requests.post(url, headers=headers, json=payload)
                
                meeting = Meeting()
                meeting.token = json.loads(response.text)['uuid']
                meeting.meeting_id = json.loads(response.text)['id']
                meeting.topic = json.loads(response.text)['topic']
                meeting.course = Course.objects.get(slug=json.loads(response.text)['agenda'])
                meeting.grade = Course.objects.get(slug=json.loads(response.text)['agenda']).grade
                meeting.start_time = json.loads(response.text)['start_time']
                meeting.duration = json.loads(response.text)['duration']
                meeting.passcode = json.loads(response.text)['password']
                meeting.join_url = json.loads(response.text)['join_url']
                meeting.save()

    # for course in teacher.course.all():
        # print(Meeting.objects.filter(course=course.id))
        # print(course.get_meetings())
    context = {
        'token' : get_token(request),
        'teacher' : teacher,
        'courses' : teacher.course.all()
    }
    return render(request, 'zoom_auth.html',context)


def delete_meeting(request):
    teacher = Teacher.objects.get(name=request.user)
    if request.method == 'POST':
        meeting_id = json.loads(request.body)['data']
        url = f"https://api.zoom.us/v2/meetings/{meeting_id}"

        # Request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {teacher.access_token}"
        }
        response = requests.delete(url, headers=headers)
        Meeting.objects.get(meeting_id=meeting_id).delete()
    return JsonResponse({'test':response.text})