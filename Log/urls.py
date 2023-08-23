from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('logout', views.logout_page, name='logout_page'),

    path('zoom', views.zoom, name='zoom_page'),
    path('zoom_auth', views.zoom_auth, name='zoom_auth_page'),
    path('delete_meeting', views.delete_meeting),
]
