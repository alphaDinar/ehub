from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,post_delete
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification,NotificationStatus
from Quiz.models import Quiz,Assignment
# from SuperManager.models import TimeTable

def create_notification(instance, message, n_type, link_slug):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'student_dash',{
            'type' : 'notify_handler',
            'message' : f'test_passed'
        }
    )
    notification = Notification()
    notification.type = n_type
    if hasattr(instance, 'grade'):
        notification.grade = instance.grade
    else:
        notification.grade = instance.course.grade
    if hasattr(instance, 'course'):
        notification.course = instance.course       
    else:
        notification.course = instance.grade.get_courses()[0] 
    notification.con = message
    notification.link_slug = link_slug 
    notification.save()
    students = []
    if hasattr(instance, 'grade'):
        students = instance.grade.get_students()
    else:
        students = instance.course.grade.get_students()

    for student in students:
        student.get_notification().note_json.append(notification.id)
        student.get_notification().counter = len(student.get_notification().note_json)
        student.get_notification().save() 


@receiver(post_save, sender=Quiz)
def notify_new_quiz(sender, instance, created ,**kwargs):
    if created:
        n_type = 'quiz'
        message = f'A new quiz has been set | title : {instance.title}'
        create_notification(instance, message, n_type, link_slug=instance.topic.slug)
        
@receiver(pre_save, sender=Quiz)
def notify_update_quiz(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        pass
    else:
        if instance.title != previous_instance.title or instance.con != previous_instance.con:
          n_type = 'quiz'
          message = f'Quiz has been updated | title : {instance.title}'
          create_notification(instance, message, n_type, link_slug=instance.topic.slug)        
        
@receiver(post_delete, sender=Quiz)
def notify_delete_quiz(sender, instance, **kwargs):
    n_type = 'quiz'
    message = f'Quiz is no longer Available | title : {instance.title}'
    create_notification(instance, message, n_type, link_slug=instance.topic.slug)




@receiver(post_save, sender=Assignment)
def notify_new_assignment(sender, instance, created ,**kwargs):
    if created:
        n_type = 'assignment'
        message = f'A new assignment has been set | title : {instance.title}'
        create_notification(instance, message, n_type, link_slug=instance.topic.slug)
        
@receiver(pre_save, sender=Assignment)
def notify_update_assignment(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        pass
    else:
        if instance.title != previous_instance.title or instance.con != previous_instance.con or instance.deadline != previous_instance.deadline:
          n_type = 'assignment'
          message = f'Assignment has been updated | title : {instance.title}'
          create_notification(instance, message, n_type, link_slug=instance.topic.slug)        
        
@receiver(post_delete, sender=Assignment)
def notify_delete_assignment(sender, instance, **kwargs):
    n_type = 'assignment'
    message = f'Assignment is no longer Available | title : {instance.title}'
    create_notification(instance, message, n_type, link_slug=instance.topic.slug)


# @receiver(post_save, sender=TimeTable)
# def notify_update_timetable(sender, instance, created, **kwargs):
#     if not created:
#         n_type = 'timetable'
#         message = f'Your Timetable has been updated'
#         create_notification(instance, message, n_type, link_slug='student_timetable')
