from django.shortcuts import render,redirect
from django.middleware.csrf import get_token
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from Log.models import Student
from Course.models import Course
from Scheme.models import Scheme
from Quiz.models import Quiz,Assignment
from SuperManager.models import Event,Notice,Grading,TimeTable
from Notification.models import Notification
from .models import SchemeProgress,QuizScore,AssignmentScore,StudentReport
import json

def checkStudent(request):
    if Student.objects.filter(name=request.user).exists():
        return True
    else:
        return False
    
def get_grade_box():
    grading_box = []    
    for grading in Grading.objects.all():
        grading_box.append({'min': grading.min_mark,'max' : grading.max_mark, 'grade' : grading.grade, 'remark' : grading.remark, 'color' : grading.color_code})
    return json.dumps(grading_box)
    
import datetime
from django.utils import timezone

def student_dash(request):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        course_progress = []
        red_assignments = []
        for course in student.grade.get_courses():
            for assignment in course.get_assignments().filter(status='pending').order_by('deadline'):
                time_left = (assignment.deadline - timezone.now()).days
                if time_left < 1:
                    red_assignments.append(assignment)

        for course in student.grade.get_courses():
            course_progress_count = []
            for progress in course.get_scheme_progress().filter(student=student):
                course_progress_count.append(progress.progress_count)
            course_progress.append(course_progress_count)
        
        events = Event.objects.filter(grade=student.grade).order_by('start_date')[:3]

        for course in student.grade.get_courses():
            print(course.get_schemes())

        quizes = []
        for course in student.grade.get_courses():
            for quiz in course.get_quizes().order_by('-id'):
                quizes.append(quiz)
        assignments = []
        for course in student.grade.get_courses():
            for assignment in course.get_assignments().filter(status='pending').order_by('deadline'):
                assignments.append(quiz)

        quiz_counter = 0 
        for quiz in quizes:
            if any(score.holder == quiz for score in student.get_quiz_scores()):
                quiz_counter += 1
        quiz_progress = {'total':len(quizes), 'attempted': quiz_counter}

        assignment_counter = 0 
        for assignment in assignments:
            if any(score.holder == assignment for score in student.get_assignment_scores()):
                assignment_counter += 1
        assignment_progress = {'total':len(assignments), 'attempted': assignment_counter}

    context = {
        'token' : get_token(request),
        'grading_box' : get_grade_box(),
        'course_progress' : course_progress,
        'events' : events,
        'red_assignments' : red_assignments[:3],
        'quizes' : quizes[:4],
        'quiz_progress' : json.dumps(quiz_progress),
        'assignment_progress' : json.dumps(assignment_progress)
    }
    return render(request, 'student_dash.html', context)

def student_sideBar(request):
    context = {
        'ball' : 'power'
    }
    return render(request, 'student_sideBar.html', context)

def end_assignment(request):
    obj_id = json.loads(request.body)['data']
    if Assignment.objects.filter(id=obj_id).exists():
        assignment = Assignment.objects.get(id=obj_id)
        Quiz.objects.create(title=assignment.title, course=assignment.course, topic=assignment.topic, con=assignment.con, marking_scheme=assignment.marking_scheme).save()
        assignment.delete()
    return JsonResponse({'test':'good'})


def student_slides(request):
    student = Student.objects.get(name=request.user)
    courses = student.grade.get_courses().all()
    course_progress = []
    for course in student.grade.get_courses():
        course_progress_count = []
        for progress in course.get_scheme_progress().filter(student=student):
            course_progress_count.append(progress.progress_count)
        course_progress.append(course_progress_count)
    context = {
        'courses' : courses,
        'course_progress' : course_progress
    }
    return render(request, 'student_slides.html', context)

def student_get_slides_schemes(request, slug):
    student = Student.objects.get(name=request.user)
    course = Course.objects.get(slug=slug)
    scheme_progress = SchemeProgress.objects.filter(student=student).filter(course=course)
    progress_list = []
    for progress in scheme_progress:
        progress_list.append(progress.progress_count)
    context = {
        'course' : course,
        'progress_list' : progress_list,
    }
    return render(request, 'student_get_slides_schemes.html', context)

def student_get_slide(request, slug):
    scheme = Scheme.objects.get(slug=slug) 
    scheme_progress_count = Student.objects.get(name=request.user).get_scheme_progress().get(scheme=scheme).progress_count
    scheme_progress_json = json.dumps(Student.objects.get(name=request.user).get_scheme_progress().get(scheme=scheme).progress_json)
    context = {
        'token' : get_token(request),
        'scheme' : scheme,
        'scheme_progress_json' : scheme_progress_json,
        'scheme_progress_count' : scheme_progress_count
    }
    return render(request, 'student_get_slide.html', context)

def toggle_res_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        scheme =  json_data[0]
        student = Student.objects.get(name=request.user)
        res_type = json_data[1]
        res_id = json_data[2]
        scheme_progress = student.get_scheme_progress().get(scheme=scheme)
        for obj in scheme_progress.progress_json:
            if obj['type'] == res_type:
                if int(obj['id']) == int(res_id):
                    if obj['status'] == 'pending':
                        obj['status'] = 'completed'
                        scheme_progress.save()
        total_res = len(scheme_progress.progress_json)
        completed_res = 0
        for obj in scheme_progress.progress_json:
            if obj['status'] == 'completed':
                completed_res = completed_res + 1
        cur_progress = (completed_res/total_res) * 100
        if not scheme_progress.progress_count == cur_progress: 
            scheme_progress.progress_count = cur_progress
            scheme_progress.save()
    return JsonResponse({'info':'feedback', 'progress_count' : scheme_progress.progress_count})

def rate_scheme(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        student = Student.objects.get(name=request.user)
        scheme = Scheme.objects.get(id=json_data[0])
        scheme_progress = student.get_scheme_progress().get(scheme=scheme)
        scheme_progress.rating = json_data[1]
        scheme_progress.save()
    return JsonResponse({'test':'good'})

def student_quizes(request):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        courses = student.grade.get_courses().all()

        progress_list = []
        for course in courses:
            total_progress = 0
            progress_count = 0
            for quiz in course.get_quizes():
                total_progress = total_progress + 1
                if QuizScore.objects.filter(student=student).filter(holder=quiz).exists():
                    progress_count = progress_count + 1
            if total_progress > 0:
                progress_list.append((progress_count/total_progress)*100)
            else:
                progress_list.append(0)
    context = {
        'courses' : courses,
        'progress_list' : json.dumps(progress_list)
    }
    return render(request, 'student_quizes.html', context)

def student_assignments(request):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        courses = student.grade.get_courses().all()
        progress_list = []
        for course in courses:
            total_progress = 0
            progress_count = 0
            for assignment in course.get_assignments():
                total_progress = total_progress + 1
                if AssignmentScore.objects.filter(student=student).filter(holder=assignment).exists():
                    progress_count = progress_count + 1
            if total_progress > 0:
                progress_list.append((progress_count/total_progress)*100)
            else:
                progress_list.append(0)
    context = {
        'courses' : courses,
        'progress_list' : json.dumps(progress_list)
    }
    return render(request, 'student_assignments.html', context)

def student_get_quizes_schemes(request,slug):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        course = Course.objects.get(slug=slug)
        schemes = Scheme.objects.filter(course=course)

        progress_list = []   
        for scheme in schemes:
            quiz_progress = 0
            quizes = Quiz.objects.filter(topic=scheme)
            if quizes.count() > 0:
                for quiz in quizes:
                    if QuizScore.objects.filter(student=student).filter(holder=quiz).exists():
                        quiz_progress = quiz_progress + 1
                progress_list.append((quiz_progress/quizes.count())*100)
            else:
                progress_list.append(0)
    context = {
        'course' : course,
        'schemes' : schemes,
        'progress_list' : progress_list
    }
    return render(request, 'student_get_quizes_schemes.html', context)

def student_get_assignments_schemes(request,slug):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        course = Course.objects.get(slug=slug)
        schemes = Scheme.objects.filter(course=course)

        progress_list = []   
        for scheme in schemes:
            assignment_progress = 0
            assignments = Assignment.objects.filter(topic=scheme)
            if assignments.count() > 0:
                for assignment in assignments:
                    if AssignmentScore.objects.filter(student=student).filter(holder=assignment).exists():
                        assignment_progress = assignment_progress + 1
                progress_list.append((assignment_progress/assignments.count())*100)
            else:
                progress_list.append(0)
    context = {
        'course' : course,
        'schemes' : schemes,
        'progress_list' : progress_list
    }
    return render(request, 'student_get_assignments_schemes.html', context)

def student_get_quizes(request,slug):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        scheme = Scheme.objects.get(slug=slug)
        high_scores = []
        attempts = []
        question_num = []
        for quiz in scheme.get_quizes():
            if quiz.con:
                question_num.append(len(json.loads(quiz.con)))
            else:
                question_num.append(0)
            attempts.append(quiz.get_quiz_scores().filter(student=student).count())
            if quiz.get_quiz_scores().filter(student=student).exists():
                high_scores.append(quiz.get_quiz_scores().filter(student=student).order_by('-mark').first().mark)
            else:
                high_scores.append('empty')
    context = {
        'scheme' : scheme,
        'high_scores' : json.dumps(high_scores),
        'attempts' : attempts,
        'question_num' : question_num,
        'grading_box' : get_grade_box()
    }
    return render(request, 'student_get_quizes.html', context)

def student_get_assignments(request,slug):
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        student = Student.objects.get(name=request.user)
        scheme = Scheme.objects.get(slug=slug)
        pend_high_scores = []
        pend_question_num = []
        pend_result_links = [] 
        comp_high_scores = []
        comp_question_num = []
        comp_result_links = []
        for assignment in scheme.get_assignments():
            if assignment.status == 'pending':
                if assignment.con:
                    pend_question_num.append(len(json.loads(assignment.con)))
                else:
                    pend_question_num.append(0)
                if assignment.get_assignment_scores().filter(student=student).exists():
                    pend_high_scores.append(assignment.get_assignment_scores().filter(student=student).order_by('-mark').first().mark)
                    pend_result_links.append(assignment.get_assignment_scores().filter(student=student).order_by('-mark').first().id)
                else:
                    pend_high_scores.append('empty')
                    pend_result_links.append('empty')
            else:
                if assignment.con:
                    comp_question_num.append(len(json.loads(assignment.con)))
                else:
                    comp_question_num.append(0)
                if assignment.get_assignment_scores().filter(student=student).exists():
                    comp_high_scores.append(assignment.get_assignment_scores().filter(student=student).order_by('-mark').first().mark)
                    comp_result_links.append(assignment.get_assignment_scores().filter(student=student).order_by('-mark').first().id)
                else:
                    comp_high_scores.append('empty')
                    comp_result_links.append('empty')
    context = {
        'scheme' : scheme,
        'pend_question_num' : json.dumps(pend_question_num),
        'pend_high_scores' : json.dumps(pend_high_scores),
        'pend_result_links' : json.dumps(pend_result_links),
        'comp_question_num' : json.dumps(comp_question_num),
        'comp_high_scores' : json.dumps(comp_high_scores),
        'comp_result_links' : json.dumps(comp_result_links),
        'grading_box' : get_grade_box()
    }
    return render(request, 'student_get_assignments.html', context)

def student_start_quiz(request,slug):
    token = get_token(request)  
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        quiz = Quiz.objects.get(slug=slug)
    context = {
        'token' : token,
        'quiz' : quiz,
    }
    return render(request, 'student_start_quiz.html', context)

def student_start_assignment(request,slug):
    token = get_token(request)  
    if not checkStudent(request):
        messages.error(request,'Login with Student Account')
        return redirect('homepage')
    else:
        assignment = Assignment.objects.get(slug=slug)
        if assignment.protection == 'unlocked':
            assignment_con = assignment.con
        else:
            assignment_con = []
    context = {
        'token' : token,
        'assignment_id' : assignment.id,
        'assignment_title' : assignment.title,
        'assignment_deadline' : assignment.deadline,
        'assignment_topic_slug' : assignment.topic.slug,
        'assignment_con' : assignment_con
    }
    return render(request, 'student_start_assignment.html', context)


def set_score(json_data,user,obj_holder,obj):
    choice_box = json.loads(json_data['data'][1])
    marking_scheme = json.loads(obj_holder.marking_scheme)
    q_num = len(marking_scheme)
    score_count = 0
    for i in range(q_num):
        if json.loads(obj_holder.con)[i]['type'] == 'fill_in_mode':
            for ii in range(len(marking_scheme[i]['cor_ans'])):
                if choice_box[i][ii].lower() ==  marking_scheme[i]['cor_ans'][ii].lower():
                    score_count = score_count + (1/(len(marking_scheme[i]['cor_ans'])))
                    print((1/(len(marking_scheme[i]['cor_ans']))))
        else:   
            if choice_box[i] == marking_scheme[i]['cor_ans']:
                score_count = score_count + 1

    percent = (score_count * 100)/q_num
    student = Student.objects.get(name=user)
    score = obj
    score.student = student
    score.holder = obj_holder
    score.course = obj_holder.topic.course
    score.scheme = obj_holder.topic
    score.con = obj_holder.con
    score.ans_box = obj_holder.marking_scheme
    score.mark = "{:.2f}".format(percent) 
    score.choice_box = json.dumps(choice_box)
    score.save()
    return score.id

def mark_quiz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        quiz = Quiz.objects.get(id=json_data['data'][0])
        score_id = set_score(json_data,request.user,quiz, QuizScore())
        return JsonResponse({'info': 'redirect', 'link' : f'/student_quiz_results/{score_id}' })

def mark_assignment(request):
    if request.method == 'POST':
        student = Student.objects.get(name=request.user)
        json_data = json.loads(request.body)
        assignment = Assignment.objects.get(id=json_data['data'][0])
        if not AssignmentScore.objects.filter(holder=assignment).filter(student=student).exists():
            score_id = set_score(json_data,request.user,assignment, AssignmentScore())
            return JsonResponse({'info': 'redirect', 'link' : f'/student_assignment_results/{score_id}' })
        else:
            return JsonResponse({'info':'You have already taken this quiz'})

def student_quiz_results(request,id):
    quiz_score = QuizScore.objects.get(id=id)
    context = {
        'quiz_score' : quiz_score,
        'grading_box' : get_grade_box()
    }
    return render(request, 'student_quiz_results.html', context)

def student_quiz_history(request,slug):
    student = Student.objects.get(name=request.user)
    quiz = Quiz.objects.get(slug=slug)
    scheme = quiz.topic
    quiz_scores = quiz.get_quiz_scores().filter(student=student)
    context = {
        'quiz' : quiz,
        'scheme' : scheme,
        'quiz_scores' : quiz_scores,
        'grading_box' : get_grade_box()
    }
    return render(request, 'student_quiz_history.html', context)

def student_assignment_results(request,id):
    assignment_score = AssignmentScore.objects.get(id=id)
    context = {
        'assignment_score' : assignment_score,
        'grading_box' : get_grade_box()
    }
    return render(request, 'student_assignment_results.html', context)

def student_timetable(request):
    student = Student.objects.get(name=request.user)
    timetable = TimeTable.objects.get(grade=student.grade)
    context = {
        'headers' : timetable.headers,
        'con' : timetable.con
    }
    return render(request, 'student_timetable.html', context)

def student_assignment_history(request,slug):
    student = Student.objects.get(name=request.user)
    assignment = Assignment.objects.get(slug=slug)
    scheme = assignment.topic
    assignment_scores = assignment.get_assignment_scores().filter(student=student)
    context = {
        
        'assignment' : assignment,
        'scheme' : scheme,
        'assignment_scores' : assignment_scores
    }
    return render(request, 'student_assignment_history.html', context)

def student_liveclasses(request):
    student = Student.objects.get(name=request.user)
    meeting_json = []
    for meeting in student.grade.get_meetings().order_by('start_time'):
        meeting_json.append({'join_url': meeting.join_url ,'topic' : meeting.topic, 'start_time' : datetime.datetime.strftime(meeting.start_time, '%Y-%m-%d %H:%M:%S'), 'course' : meeting.course.subject})
    context ={
        'meetings' : student.grade.get_meetings().order_by('start_time')[0:2],
        'meeting_json' : json.dumps(meeting_json)
    }
    return render(request, 'student_liveclasses.html', context)

def student_assessment(request):
    student = Student.objects.get(name=request.user)
    grade = student.grade
    quiz_course_avg_list = []
    for course in grade.get_courses():
        course_quiz_total = 0
        for scheme in course.get_schemes():
            for quiz in scheme.get_quizes():
                if quiz.get_quiz_scores().filter(student=student).exists():
                    high_score = quiz.get_quiz_scores().filter(student=student).order_by('-mark').first().mark
                    course_quiz_total = course_quiz_total + high_score
        if course.get_quizes().count() > 0:
            quiz_course_avg_list.append(course_quiz_total/course.get_quizes().count())
        else:
            quiz_course_avg_list.append(course_quiz_total)
    assignment_course_avg_list = []
    for course in grade.get_courses():
        course_assignment_total = 0
        for scheme in course.get_schemes():
            for assignment in scheme.get_assignments():
                if assignment.get_assignment_scores().filter(student=student).exists():
                    high_score = assignment.get_assignment_scores().filter(student=student).order_by('-mark').first().mark
                    course_assignment_total = course_assignment_total + high_score
        if course.get_assignments().count() > 0:
            assignment_course_avg_list.append(course_assignment_total/course.get_assignments().count())
        else:
            assignment_course_avg_list.append(course_assignment_total)
    
    context = {
        'grade' : grade,
        'quiz_course_avg_list' : json.dumps(quiz_course_avg_list),
        'assignment_course_avg_list' : json.dumps(assignment_course_avg_list),
        'grading_box' : get_grade_box()
    }
    return render(request, 'student_assessment.html', context)

def student_assessment_quizes(request,slug):
    course = Course.objects.get(slug=slug)
    context = {
        'course' : course
    }
    return render(request, 'student_assessment_quizes.html', context)

def student_events(request):
    grade = Student.objects.get(name=request.user).grade
    events_json = []
    for event in Event.objects.filter(grade=grade):
        events_json.append({'name':event.name, 'start_date':datetime.datetime.strftime(event.start_date, '%Y-%m-%d %H:%M:%S'), 'end_date' : datetime.datetime.strftime(event.end_date, '%Y-%m-%d %H:%M:%S'), 'color' : event.color})
    
    quick_events = Event.objects.filter(grade=grade).order_by('start_date')[:3]
    context = {
        'events' : json.dumps(events_json),
        'quick_events' : quick_events
    }
    return render(request, 'student_events.html', context)

def student_inbox(request):
    student = Student.objects.get(name=request.user)
    grade = student.grade
    context = {
        'grade' : grade,
    }

    return render(request, 'student_inbox.html', context)

def student_index(request):
    student = Student.objects.get(name=request.user)
    grade = student.grade
# for course in grade.get_courses():
    #     print(course.get_teacher(), course.subject)
    # print(grade.get_courses())
    progress_list = []
    for progress in SchemeProgress.objects.filter(student=student).order_by('scheme'):
        progress_list.append({'id' : progress.scheme.id, 'rating' : progress.rating})

    print(progress_list)
    context = {
        'courses' : grade.get_courses(),
        'progress_list' : json.dumps(progress_list)
    }


def student_notification(request):
    student = Student.objects.get(name=request.user)
    note_box = []
    for note_id in student.get_notification().note_json:
        note_box.append(Notification.objects.get(id=note_id))

    context ={
        'token' : get_token(request),
        'note_box' : note_box
    }
    return render(request, 'student_notification.html', context)

def toggle_note(request):
    if request.method == 'POST':
        student = Student.objects.get(name=request.user)
        json_data = int(json.loads(request.body)['data'])
        for note in student.get_notification().note_json:
            if note == json_data:
                student.get_notification().note_json.remove(note)
        student.get_notification().counter = len(student.get_notification().note_json)
        student.get_notification().save()
    return JsonResponse({'test':'good'})

def clear_notes(request):
    if request.method == 'POST':
        student = Student.objects.get(name=request.user)
        student.get_notification().note_json = []
        student.get_notification().counter = len(student.get_notification().note_json)
        student.get_notification().save()
    return JsonResponse({'test':'clear_notes'})

def student_noticeboard(request):
    context = {
        'notices' : Notice.objects.filter(grade=Student.objects.get(name=request.user).grade)
    }
    return render(request, 'student_noticeboard.html',context)

def student_report(request):
    grade = Student.objects.get(name=request.user).grade
    context = {
        'grade' : grade
    }
    return render(request, 'student_report.html', context)


def mark2(request):
    student = Student.objects.get(name=request.user)
    context = {
        'student' : student
    }
    return render(request, 'mark2.html', context)