from django.shortcuts import render,redirect
from django.middleware.csrf import get_token
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Course.models import Course,Grade
from Log.models import Student,User,Teacher,Manager
from Scheme.models import Scheme
from Student.models import SchemeProgress
from .models import Event,Notice,Grading,TimeTableTemplate,TimeTable
from Notification.models import NotificationStatus
import json,datetime
from django.utils import timezone

@login_required
def supermanager(request):
    if not request.user.is_superuser:
        logout(request)
        return redirect('homepage')
    return render(request, 'supermanager.html')

@login_required
def super_student_assessment(request):
    grades = Grade.objects.all()
    context = {
        'grades' : grades
    }
    return render(request, 'super_student_assessment.html', context)

@login_required
def super_get_student_assessment(request,slug):
    grade = Grade.objects.get(slug=slug)
    context = {
        'grade' : grade
    }
    return render(request, 'super_get_student_assessment.html', context)

@login_required
def super_add_student(request):
    grades = Grade.objects.all()
    context = {
        'grades' : grades
    }
    return render(request, 'super_add_student.html', context)

def capitalize(string):
    return string[0].upper() + string[1:]

@login_required
def super_get_students(request,slug):
    grade = Grade.objects.get(slug=slug)
    print(grade.get_courses())

    token = get_token(request)
    if request.method == 'POST':
        if request.POST.get('type') == 'new':
            if User.objects.filter(username=request.POST.get('first_name')).exists():
                messages.error(request, 'student already exists')
            else:
                user = User()
                user.username = f"{request.POST.get('first_name')}{User.objects.count() + 1}".lower()
                user.password = make_password(request.POST.get('last_name'))
                user.save()
                student = Student()
                student.name = user
                student.grade = grade
                student.first_name = capitalize(request.POST.get('first_name'))
                student.last_name = capitalize(request.POST.get('last_name'))
                student.save()
                NotificationStatus.objects.create(student=student).save()                
                for course in student.grade.get_courses():
                    for scheme in course.get_schemes():
                        if not SchemeProgress.objects.filter(student=student).filter(scheme=scheme).exists():
                            SchemeProgress.objects.create(student=student,course=scheme.course, scheme=scheme).save()
                for progress in SchemeProgress.objects.filter(student=student):
                    scheme = Scheme.objects.get(id=progress.scheme.id)
                    progress.progress_json = []
                    for image in scheme.get_images():
                        progress.progress_json.append({'type':'image','id' : image.id, 'status' : 'pending'})
                    for video in scheme.get_videos():
                        progress.progress_json.append({'type':'video','id' : video.id, 'status' : 'pending'})
                    for passage in scheme.get_passages():
                        progress.progress_json.append({'type':'passage','id' : passage.id, 'status' : 'pending'})
                    for slide in scheme.get_slides():
                        progress.progress_json.append({'type':'slide','id' : slide.id, 'status' : 'pending'})
                    progress.save()
                
                messages.success(request, f'{user.username} Created successfully')
        else :
            user = User.objects.get(username=request.POST.get('name'))
            user.password = make_password(request.POST.get('last_name'))
            user.save()
            student = Student.objects.get(name=user)
            student.first_name = capitalize(request.POST.get('first_name'))
            student.last_name = capitalize(request.POST.get('last_name'))
            student.save()
            messages.success(request, f'{student} Updated successfully')
    context = {
        'grade' : grade,
        'token' : token
    }
    return render(request, 'super_get_students.html', context)

@login_required
def super_add_teacher(request):
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    token = get_token(request)
    super_add(request, Teacher, 'teacher')
    context = {
        'teachers' : teachers,
        'courses' : courses,
        'token' : token
    }
    return render(request, 'super_add_teacher.html', context)

@login_required
def super_add_manager(request):
    managers = Manager.objects.all()
    courses = Course.objects.all()
    token = get_token(request)
    super_add(request, Manager, 'manager')    
    context = {
        'managers' : managers,
        'courses' : courses,
        'token' : token
    }
    return render(request, 'super_add_manager.html', context)

@login_required
def super_add(request , Staff, status):
    if request.method == 'POST':
        if request.POST.get('type') == 'new':
            if User.objects.filter(username=request.POST.get('username')).exists():
                messages.error(request, 'Username already Taken')
            else:
                if(request.POST.getlist('courses')):
                    courseList = request.POST.getlist('courses')
                    user = User()
                    user.username = request.POST.get('username')
                    user.password = make_password(request.POST.get('password'))
                    user.save()
                    staff = Staff()
                    staff.name = user
                    staff.password = request.POST.get('password')
                    staff.save()
                    courseList = request.POST.getlist('courses')
                    for course_obj in courseList:
                        course = Course.objects.get(id=course_obj)
                        if status == 'teacher':
                            course.teacher = staff
                        else:
                            course.manager = staff
                        course.save()
                    messages.info(request, f'{user.username} Created successfully')
                else:
                    messages.error(request, 'Select at least one Course')
        else:
            courseList = request.POST.getlist('courses')
            user = User.objects.get(username=request.POST.get('name'))
            user.username = request.POST.get('username')
            user.password = make_password(request.POST.get('password'))
            # user.save()
            staff = Staff.objects.get(name=user)
            staff.password = request.POST.get('password')
            # staff.save()
            for course in staff.get_courses():
                if status == 'teacher':
                    course.teacher = None
                    course.save()
                else:
                    course.manager = None
                    course.save()

            for course_obj in courseList:
                course = Course.objects.get(id=course_obj)
                if status == 'teacher':
                    course.teacher = staff
                else:
                    course.manager = staff
                course.save()            
            messages.success(request, f'{user} Updated successfully')

@login_required
def super_delete_user(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        User.objects.get(username=json_data['data']).delete()
    return JsonResponse({'info':'success'})


@login_required
def super_grades(request):
    grades = Grade.objects.all()
    token = get_token(request)
    if request.method == 'POST':
            if request.POST.get('type') == 'new':
                if Grade.objects.filter(name=request.POST.get('grade')).exists() or Grade.objects.filter(code=request.POST.get('code')).exists():
                    messages.error(request, 'Grade already exists')
                grade = Grade()
                grade.name = request.POST.get('grade')
                grade.code = request.POST.get('code')
                grade.save()
            else:
                grade = Grade.objects.get(id=request.POST.get('id'))
                grade.name = request.POST.get('grade')
                grade.code = request.POST.get('code')
                grade.save()
    context = {
        'grades' : grades,
        'token' : token
    }
    return render(request, 'super_grades.html', context)

@login_required
def super_get_grade(request,slug):
    grade = Grade.objects.get(slug=slug)
    token = get_token(request)
    if request.method == 'POST':
        if Course.objects.filter(grade=grade).filter(subject=request.POST.get('subject')).exists():
            messages.error(request, 'Course already exists')
        else:
            if request.POST.get('type') == 'new':
                course = Course()
                course.subject = request.POST.get('subject')
                course.grade = grade
                course.save()
                messages.success(request, 'Course added successfully')
            else:
                course = Course.objects.get(id=request.POST.get('id'))
                course.subject = request.POST.get('subject')
                course.save()
                messages.success(request, 'Course updated successfully')
    context = {
        'grade' : grade,
        'token' : token
    }
    return render(request, 'super_get_grade.html', context)

@login_required
def super_delete_grade(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        Grade.objects.get(id=json_data['data']).delete()
    return JsonResponse({'test':'good'})

@login_required
def super_courses(request):
    courses = Course.objects.all().order_by('abb')
    token = get_token(request)
    context = {
        'courses' : courses,
        'token' : token
    }
    return render(request, 'super_courses.html', context)

@login_required
def super_delete_course(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        Course.objects.get(id=json_data['data']).delete()
    return JsonResponse({'test':'good'})



def get_event_json(events):
    events_json = []
    for event in events:
        events_json.append({'id':event.id ,'name':event.name, 'start_date' : datetime.datetime.strftime(event.start_date, '%Y-%m-%d %H:%M:%S'), 'end_date' : datetime.datetime.strftime(event.end_date, '%Y-%m-%d %H:%M:%S'), 'color':event.color})
    return events_json

# @login_required
def super_events(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'new':
            event = Event()
        else:
            event = Event.objects.get(id=request.POST.get('id'))
        event.name = request.POST.get('name')        
        event.start_date = datetime.datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        event.end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
        event.color = request.POST.get('color')
        event.save()
        event.grade.set(Grade.objects.all())

    event_json = get_event_json(Event.objects.all())

    context = {
        'token' : get_token(request) ,
        'events' : json.dumps(event_json),
        'event_count' : len(event_json)
    }
    return render(request, 'super_events.html', context)

def super_delete_event(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        Event.objects.get(id=json_data).delete()
    return JsonResponse({'test':'good'})

def super_noticeboard(request):
    context = {
        'notices' : Notice.objects.all() 
    }
    return render(request, 'super_noticeboard.html', context)

@login_required
def super_grading(request):
    if request.method == 'POST':
        if request.POST.get('type') == 'new':
            if Grading.objects.filter(grade=request.POST.get('grade')):
                messages.error(request, 'Grade already exists')
            else:
                grading = Grading()
                messages.success(request, 'Grade added successfully')
        else:
            grading = Grading.objects.get(id=request.POST.get('id'))
            messages.success(request, 'Grade updated successfully')
        grading.grade = request.POST.get('grade')
        grading.min_mark = request.POST.get('min_mark')
        grading.max_mark = request.POST.get('max_mark')
        grading.remark = request.POST.get('remark')
        grading.color_code = request.POST.get('color_code')
        grading.save()
        
    context = {
        'token' : get_token(request),
        'gradings' : Grading.objects.all().order_by('-min_mark') 
    }
    return render(request, 'super_grading.html', context)

@login_required
def super_delete_grading(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        Grading.objects.get(id=json_data['data']).delete()
    return JsonResponse({'test':'good'})

def super_timetable(request):
    context = {
        'token' : get_token(request),
        'grades' : Grade.objects.all(),
        'table_template' : TimeTableTemplate.objects.last()
    }
    return render(request, 'super_timeTable.html', context)

def super_timetable_template(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        if TimeTableTemplate.objects.count() > 0:
            TimeTableTemplate.objects.first().delete()
        TimeTableTemplate.objects.create(headers=json_data[0], con=json_data[1]).save()
    return JsonResponse({'test':'template'})

def super_make_timetable(request,slug):
    grade = Grade.objects.get(slug=slug)
    if TimeTable.objects.filter(grade=grade).exists():
        gradeTimetable = TimeTable.objects.get(grade=grade)
    else:
        gradeTimetable = ''
    if request.method == 'POST':
        if TimeTable.objects.filter(grade=grade).exists():
            gradeTimetable = TimeTable.objects.get(grade=grade)
            gradeTimetable.headers = ''
            gradeTimetable.con = ''
            gradeTimetable.save()
    context = {
        'token' : get_token(request),
        'grade' : grade,
        'gradeTimetable' : gradeTimetable,
        'table_template' : TimeTableTemplate.objects.last()
    }
    return render(request, 'super_make_timeTable.html', context)

def super_save_timetable(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        grade = Grade.objects.get(id=json_data[0])
        if TimeTable.objects.filter(grade=grade).exists():
            timetable = TimeTable.objects.get(grade=grade)
            timetable.headers = json_data[1][0]
            timetable.con = json_data[1][1]
            timetable.save()
        else:
            TimeTable.objects.create(grade=grade, headers=json_data[1][0], con=json_data[1][1]).save()
    return JsonResponse({'test':'save_table'})



def super_admin(request):
    context = {
        'teachers' : Teacher.objects.all(),
        'managers' : Manager.objects.all(),
        'students' : Student.objects.all() 
    }
    return render(request, 'super_admin.html', context)

def super_test(request):
    student = Student.objects.get(name=request.user)
    context = {
        'student' : student
    }
    return render(request, 'super_test.html', context)

