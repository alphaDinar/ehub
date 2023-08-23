from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Log.models import User,Teacher, Manager

@login_required
def courses(request):
    user = User.objects.get(username=request.user)
    if Teacher.objects.filter(name=user.id).exists():
        staff = Teacher.objects.get(name=user.id)
    else:
        staff = Manager.objects.get(name=user.id)
    courses = staff.course.all()
    context = {
        'courses' : courses
    }
    return render(request, 'courses.html', context)