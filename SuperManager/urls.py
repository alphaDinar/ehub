from django.urls import path
from . import views

urlpatterns = [
    path('supermanager', views.supermanager, name='supermanager_page'),
    
    path('super_student_assessment', views.super_student_assessment, name='super_student_assessment_page'),
    path('super_get_student_assessment/<str:slug>', views.super_get_student_assessment, name='super_get_student_assessment_page'),

    path('super_add_student', views.super_add_student, name='super_add_student_page'),
    path('super_get_students/<str:slug>', views.super_get_students, name='super_get_students_page'),

    path('super_add_teacher', views.super_add_teacher, name='super_add_teacher_page'),
    # path('super_get_teachers/<str:slug>', views.super_get_teachers, name='super_get_teachers_page'),

    path('super_add_manager', views.super_add_manager, name='super_add_manager_page'),

    path('super_delete_user', views.super_delete_user),

    path('super_grades/', views.super_grades, name='super_grades_page'),
    path('super_delete_grade', views.super_delete_grade),

    path('super_get_grade/<str:slug>', views.super_get_grade, name='super_get_grade_page'),
    path('super_delete_course', views.super_delete_course),

    path('super_courses', views.super_courses, name='super_courses_page'),

    path('super_events', views.super_events, name='super_events_page'),
    path('super_delete_event', views.super_delete_event),

    path('super_noticeboard', views.super_noticeboard, name='super_noticeboard_page'),

    path('super_grading', views.super_grading, name='super_grading_page'),
    path('super_delete_grading', views.super_delete_grading),

    path('super_timetable', views.super_timetable, name='super_timetable_page'),
    path('super_timetable_template', views.super_timetable_template),
    path('super_make_timetable/<str:slug>', views.super_make_timetable, name='super_make_timeTable_page'),
    path('super_save_timetable', views.super_save_timetable),
    
    path('super_admin', views.super_admin, name='super_admin_page'),

    path('super_test', views.super_test, name='super_test_page'),

]
