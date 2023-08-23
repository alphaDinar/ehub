from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SuperManager.urls')),
    path('', include('Log.urls')),
    path('', include('Course.urls')),
    path('', include('Scheme.urls')),
    path('', include('Quiz.urls')),
    path('',include('Student.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
