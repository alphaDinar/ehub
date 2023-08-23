from django.middleware.csrf import get_token
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from Log.models import Teacher,Student
from Course.models import Course
from Scheme.models import Scheme,Image,Video,Passage,Pdf,Slide,RecentScheme
from Student.models import SchemeProgress
import json

@login_required
def schemes(request,slug):
    course = Course.objects.get(slug = slug)
    schemes = course.get_schemes()
    pend_count = schemes.filter(status = 'pending').count()
    act_count = schemes.filter(status = 'active').count()
    comp_count = schemes.filter(status = 'completed').count()
    status = {'pend_count' : pend_count, 'act_count' : act_count, 'comp_count' : comp_count}
    recent_scheme = ''
    if request.user.is_teacher:
        if RecentScheme.objects.filter(teacher=Teacher.objects.get(name=request.user)).exists():
            recent_scheme = RecentScheme.objects.filter(teacher=Teacher.objects.get(name=request.user)).last()
            
    if request.method == 'POST':
        name = request.POST.get('name').capitalize()
        if Scheme.objects.filter(topic = name).exists():
            messages.error(request, f'{name} Already Exists')
        else:
            if request.POST.get('type') == 'new':
                scheme = Scheme.objects.create(topic = name, course = course)
                scheme.save()
                for student in Student.objects.filter(grade=scheme.course.grade):
                    SchemeProgress.objects.create(student=student, scheme=scheme, course=scheme.course).save()
                messages.success(request, f'{name} Created Successfully')
            else:
                scheme = Scheme.objects.get(id=request.POST.get('id'))
                scheme.topic = name
                scheme.save()
                messages.success(request, f'Scheme Updated Successfully')
    context = {
        'course' : course,
        'schemes' : schemes,
        'status' : status,
        'recent_scheme' : recent_scheme,
        'token' : get_token(request)
    }
    return render(request, 'schemes.html', context)

def delete_scheme(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        Scheme.objects.get(id=json_data).delete()
        return JsonResponse({'test' : 'good'})

def use_scheme(request, slug):
    scheme = Scheme.objects.get(slug=slug)
    teacher = Teacher.objects.get(name=request.user)
    if RecentScheme.objects.filter(teacher=teacher).exists():
        RecentScheme.objects.filter(teacher=teacher).delete()
    RecentScheme.objects.create(teacher=teacher, scheme=scheme).save()
    token = get_token(request)
    context ={
        'scheme' : scheme,
        'token' : token
    }
    return render(request, 'use_scheme.html', context)

def add_progress_res(scheme_progress, progress_json):
    for progress in scheme_progress:
        if progress.progress_json:
            progress.progress_json.append(progress_json)
            total_res = len(progress.progress_json)
            completed_res = 0
            for obj in progress.progress_json:
                if obj['status'] == 'completed':
                    completed_res = completed_res + 1
            cur_progress = (completed_res/total_res) * 100
            print(cur_progress)
            if not progress.progress_count == cur_progress: 
                progress.progress_count = cur_progress
        else:
            progress.progress_json = [progress_json]
        progress.save()

def save_scheme_slide(request):
    if request.method == 'POST':
        data = request.body
        json_data = json.loads(data)
        scheme = Scheme.objects.get(id=json_data['data'][0])
        if json_data['data'][1]:
            slide_title = json_data['data'][1]
        else:
            slide_title = 'New Slide'
        if Slide.objects.filter(holder=scheme).filter(title=slide_title).exists():
            slide = Slide.objects.get(title=slide_title)
            slide.con = json_data['data'][2]   
            slide.save() 
        else:
            slide = Slide.objects.create(title=slide_title, con=json_data['data'][2], holder=scheme)
            slide.save()
            scheme_progress = SchemeProgress.objects.filter(scheme=scheme)
            progress_json = {'type':'slide','id' : slide.id, 'status' : 'pending'}
            add_progress_res(scheme_progress, progress_json)
            
    return JsonResponse({'test':'good'})

def edit_scheme(request, slug):
    scheme = Scheme.objects.get(slug=slug)
    token = get_token(request)
    scheme_progress = SchemeProgress.objects.filter(scheme=scheme)

    if request.method == 'POST':
        if request.POST.get('res_type') == 'image':
            res_name = request.POST.get('res_name')
            if Image.objects.filter(holder=scheme).filter(name=res_name).exists():
                messages.info(request, f'Image named {res_name} already exists')
            else:
                image = Image()
                image.name = res_name
                image.image = request.FILES.get('res')
                image.holder = scheme
                image.save()
                progress_json = {'type':'image','id' : image.id, 'status' : 'pending'}
                add_progress_res(scheme_progress, progress_json)
                messages.info(request, 'images added successfully')
        elif request.POST.get('res_type') == 'video':
            res_name = request.POST.get('res_name')
            if Video.objects.filter(holder=scheme).filter(name=res_name).exists():
                messages.info(request, f'Video named {res_name} already exists')
            else:
                video = Video()
                video.name = request.POST.get('res_name')
                video.video = request.FILES.get('res')
                video.holder = scheme
                video.save()
                progress_json = {'type':'video','id' : video.id, 'status' : 'pending'}
                add_progress_res(scheme_progress, progress_json)
                messages.info(request, 'video added successfully')
        elif request.POST.get('res_type') == 'passage':
            if(request.POST.get('passage_id')):
                passage = Passage.objects.get(id=request.POST.get('passage_id'))
                passage.title = request.POST.get('passage_title')
                passage.body = request.POST.get('passage_body')
                if request.FILES.get('passage_thumb'):
                    passage.thumb = request.FILES.get('passage_thumb')
                passage.save()
                messages.info(request, 'changes have been made')
            else:
                res_name = request.POST.get('passage_title')
                if Passage.objects.filter(holder=scheme).filter(title=res_name).exists():
                    messages.info(request, f'Passage named {res_name} already exists')
                else:
                    passage = Passage()
                    passage.title = res_name
                    passage.body = request.POST.get('passage_body')
                    if request.FILES.get('passage_thumb'):
                        passage.thumb = request.FILES.get('passage_thumb') 
                    passage.holder = scheme
                    passage.save()
                    progress_json = {'type':'passage','id' : passage.id, 'status' : 'pending'}
                    add_progress_res(scheme_progress, progress_json)
                    messages.info(request, 'passage added successfully')
        elif request.POST.get('res_type') == 'pdf':
            res_name = request.POST.get('name')
            if Pdf.objects.filter(holder=scheme).filter(name=res_name).exists():
                messages.info(request, f'Pdf named {res_name} already exists')
            else:
                pdf = Pdf()
                pdf.name = res_name
                pdf.pdf = request.FILES['res']
                pdf.holder = scheme
                pdf.save()
                messages.info(request, 'PDF added successfully')
    context ={
        'scheme' : scheme,
        'token' : token
    }   
    return render(request, 'edit_scheme.html', context)


def remove_progress_obj(scheme, obj_type, res_id):
    scheme_progress = SchemeProgress.objects.filter(scheme=scheme)
    for progress in scheme_progress:
        for obj in progress.progress_json:
            if obj['type'] == obj_type:
                if int(obj['id']) == int(res_id):
                    progress.progress_json.remove(obj)
                    progress.save()

def delete_scheme_image(request):
    if request.method == 'POST':
        data = request.body
        json_data = json.loads(data)
        res_id = json_data['data']
        scheme = Image.objects.get(id=res_id).holder
        obj_type = 'image'
        remove_progress_obj(scheme, obj_type, res_id) 
        Image.objects.get(id=res_id).delete()
    return JsonResponse({'test':'good'})

def delete_scheme_video(request):
    if request.method == 'POST':
        data = request.body
        json_data = json.loads(data)
        res_id = json_data['data']
        scheme = Video.objects.get(id=res_id).holder
        obj_type = 'video'
        remove_progress_obj(scheme, obj_type, res_id) 
        Video.objects.get(id=res_id).delete()
    return JsonResponse({'test':'good'})

def delete_scheme_passage(request):
    if request.method == 'POST':
        data = request.body
        json_data = json.loads(data)
        res_id = json_data['data']
        scheme = Passage.objects.get(id=res_id).holder
        obj_type = 'passage'
        remove_progress_obj(scheme, obj_type, res_id) 
        Passage.objects.get(id=res_id).delete()
    return JsonResponse({'test':'good'})

def delete_scheme_pdf(request):
    if request.method == 'POST':
        data = request.body
        json_data = json.loads(data)
        res_id = json_data['data']
        Pdf.objects.get(id=res_id).delete()
    return JsonResponse({'test':'good'})

def delete_scheme_slide(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)['data']
        res = Slide.objects.get(id = json_data)
        scheme = res.holder
        obj_type = 'slide'
        remove_progress_obj(scheme, obj_type, res.id) 
        res.delete()
    return JsonResponse({'info':'delete'})


