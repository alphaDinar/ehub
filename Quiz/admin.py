from django.contrib import admin
from .models import Quiz,Assignment,AssignmentSession

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title','created_on')
    class Meta:
        model = Quiz

admin.site.register(Quiz, QuizAdmin)

admin.site.register(Assignment)
admin.site.register(AssignmentSession)

