from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib import messages
from celery import shared_task
from Course.models import Course
from Scheme.models import Scheme
from Quiz.models import Quiz,Assignment
from Student.models import QuizScore,AssignmentScore 
from SuperManager.models import Grading
from django.utils import timezone
import json,datetime
from datetime import timedelta

def get_grade_box():
    grading_box = []    
    for grading in Grading.objects.all():
        grading_box.append({'min': grading.min_mark,'max' : grading.max_mark, 'grade' : grading.grade, 'remark' : grading.remark, 'color' : grading.color_code})
    return json.dumps(grading_box)


def quizes(request,slug):
    course = Course.objects.get(slug=slug)
    if request.user.is_manager:
        return redirect('schemes_page', course.slug)
    schemes = course.get_schemes()
    quiz_count = 0
    for scheme in schemes:
        quiz_count = quiz_count + scheme.get_quizes().count()
    context ={
        'course' : course,
        'schemes' : schemes,
        'quiz_count' : quiz_count,
    }
    return render(request, 'quizes.html', context)

def assignments(request,slug):
    course = Course.objects.get(slug=slug)
    if request.user.is_manager:
        return redirect('schemes_page', course.slug)
    context ={
        'course' : course,
        'schemes' : course.get_schemes(),
    }
    return render(request, 'assignments.html', context)

def get_quizes(request,slug):
    scheme = Scheme.objects.get(slug=slug)
    q_count_list = []
    for quiz in scheme.get_quizes():
        if len(quiz.con) > 0:
            q_count =  len(json.loads(quiz.con))
            q_count_list.append(q_count)
        else:
            q_count_list.append(0)    

    course = scheme.course
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        print(title)
        if not Quiz.objects.filter(topic=scheme).filter(title=title).exists():
            Quiz.objects.create(topic=scheme,title=title, course=scheme.course).save()
        else:
            messages.error(request, f'Quiz with title {title} already exists')
    context ={
        'course' : course,
        'scheme' : scheme,
        'q_count_list' : json.dumps(q_count_list)
    }
    return render(request, 'get_quizes.html', context)

def get_assignments(request,slug):
    scheme = Scheme.objects.get(slug=slug)
    course = scheme.course
    if request.method == 'POST':
        title = request.POST.get('title').capitalize()
        if not Assignment.objects.filter(topic=scheme).filter(title=title).exists():
            Assignment.objects.create(topic=scheme,title=title, course=scheme.course, deadline=timezone.now() + timedelta(hours=2)).save()
        else:
            messages.error(request, f'Quiz with title {title} already exists')
    context ={
        'course' : course,
        'scheme' : scheme,
    }
    return render(request, 'get_assignments.html', context)

def use_quiz(request,slug):
    quiz = Quiz.objects.get(slug=slug)
    token = get_token(request)  
    if request.method == 'POST':
        quiz.title = request.POST.get('title')
        quiz.duration = request.POST.get('duration')
        quiz.save()
    context = {
        'token' : token,
        'quiz' : quiz,
    }
    return render(request, 'use_quiz.html', context)

def use_assignment(request,slug):
    assignment = Assignment.objects.get(slug=slug)
    token = get_token(request)  
    if request.method == 'POST':
        assignment.title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        deadline = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
        assignment.deadline = deadline
        assignment.save()
    context = {
        'token' : token,
        'assignment' : assignment,
    }
    return render(request, 'use_assignment.html', context)

def toggle_assignment(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        assignment = Assignment.objects.get(id=json_data['data'][0])
        print(assignment)
        if assignment.protection == 'locked':
            assignment.protection = 'unlocked'
        else:
            assignment.protection = 'locked'
        assignment.save()
    return JsonResponse({'test':'good'})

def delete_quiz(request,slug):
    quiz = Quiz.objects.get(slug=slug)
    scheme = quiz.topic.slug
    quiz.delete()
    return redirect('get_quizes_page', scheme)

def delete_assignment(request,slug):
    assignment = Assignment.objects.get(slug=slug)
    scheme = assignment.topic.slug
    assignment.delete()
    return redirect('get_assignments_page', scheme)

def set_quiz(request,slug):
    token = get_token(request)
    quiz = Quiz.objects.get(slug=slug)
    context = {
        'quiz' : quiz,
        'token' : token
    }
    return render(request, 'set_quiz.html', context)

def set_assignment(request,slug):
    token = get_token(request)
    assignment = Assignment.objects.get(slug=slug)
    context = {
        'assignment' : assignment,
        'token' : token
    }
    return render(request, 'set_assignment.html', context)

def save_quiz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        quiz = Quiz.objects.get(id=json_data['data'][0])
        quiz.con = json_data['data'][1]
        quiz.marking_scheme = json_data['data'][2]
        quiz.save()
    return JsonResponse({'info':'reload'})

def save_assignment(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        assignment = Assignment.objects.get(id=json_data['data'][0])
        assignment.con = json_data['data'][1]
        assignment.marking_scheme = json_data['data'][2]
        assignment.save()
    return JsonResponse({'info':'reload'})

def delete_session(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        quiz = Quiz.objects.get(id=json_data['data'][0])
        quiz.status = 'locked'
        quiz.save()
    return JsonResponse({'test':'deleted'})

def assess_quiz(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    course = quiz.topic.course
    quiz_scores = []
    for score in QuizScore.objects.filter(holder=quiz).order_by('-mark'):
        err = 0
        if len(quiz_scores) > 0:
            for item in quiz_scores:
                if item.student == score.student:
                    err = 1
        if err > 0:
            continue
        else:
            quiz_scores.append(score)
    for student in course.grade.get_students():
        if not QuizScore.objects.filter(student=student).filter(holder=quiz).order_by('-mark').exists():
            quiz_scores.append(student)
    context = {
        'course' : course,
        'quiz' : quiz,
        'quiz_scores' : quiz_scores,
        'grading_box' : get_grade_box()
    }
    return render(request, 'assess_quiz.html', context)

def assess_assignment(request, slug):
    assignment = Assignment.objects.get(slug=slug)
    course = assignment.topic.course
    assignment_scores = []
    for score in AssignmentScore.objects.filter(holder=assignment).order_by('-mark'):
        err = 0
        if len(assignment_scores) > 0:
            for item in assignment_scores:
                if item.student == score.student:
                    err = 1
        if err > 0:
            continue
        else:
            assignment_scores.append(score)
    for student in course.grade.get_students():
        if not AssignmentScore.objects.filter(student=student).filter(holder=assignment).order_by('-mark').exists():
            assignment_scores.append(student)
    context = {
        'course' : course,
        'assignment' : assignment,
        'assignment_scores' : assignment_scores,
        'grading_box' : get_grade_box()
    }
    return render(request, 'assess_assignment.html', context)