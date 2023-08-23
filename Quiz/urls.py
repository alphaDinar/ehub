from django.urls import path
from . import views

urlpatterns = [
    path('quizes/<str:slug>', views.quizes, name='quizes_page'),
    path('get_quizes/<str:slug>', views.get_quizes, name='get_quizes_page'),
    path('use_quiz/<str:slug>', views.use_quiz, name='use_quiz_page'),
    # path('update_quiz', views.update_quiz),
    path('delete_quiz/<str:slug>', views.delete_quiz, name='delete_quiz_page'),
    path('set_quiz/<str:slug>', views.set_quiz, name='set_quiz_page'),
    path('save_quiz', views.save_quiz),
    path('delete_session', views.delete_session),
    path('assess_quiz/<str:slug>', views.assess_quiz, name='assess_quiz_page'),


    path('assignments/<str:slug>', views.assignments, name='assignments_page'),
    path('get_assignments/<str:slug>', views.get_assignments, name='get_assignments_page'),
    path('use_assignment/<str:slug>', views.use_assignment, name='use_assignment_page'),
    path('toggle_assignment', views.toggle_assignment),
    path('delete_assignment/<str:slug>', views.delete_assignment, name='delete_assignment_page'),
    path('set_assignment/<str:slug>', views.set_assignment, name='set_assignment_page'),
    path('save_assignment', views.save_assignment),
    path('assess_assignment/<str:slug>', views.assess_assignment, name='assess_assignment_page'),

    # path('assess_quiz/<str:slug>', views.assess_quiz, name='assess_quiz_page'),
]
