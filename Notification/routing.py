from django.urls import path
from . import consumers 

websocket_urlpatterns = [
    path('ws/student_dash', consumers.StudentDashConsumer.as_asgi()),
]