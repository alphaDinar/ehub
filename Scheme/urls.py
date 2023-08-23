from django.urls import path
from . import views

urlpatterns = [
    path('schemes/<str:slug>', views.schemes, name='schemes_page'),
    path('delete_scheme', views.delete_scheme),

    path('use_scheme/<str:slug>', views.use_scheme, name='use_scheme_page'),
    path('save_scheme_slide', views.save_scheme_slide),
    path('delete_scheme_slide', views.delete_scheme_slide),

    path('edit_scheme/<str:slug>', views.edit_scheme, name='edit_scheme_page'),
    path('delete_scheme_image', views.delete_scheme_image),
    path('delete_scheme_video', views.delete_scheme_video),
    path('delete_scheme_passage', views.delete_scheme_passage),
    path('delete_scheme_pdf', views.delete_scheme_pdf),

    # path('edit_scheme/<str:slug>/delete_video/<int:id>', views.delete_video, name='delete_video'),
]
