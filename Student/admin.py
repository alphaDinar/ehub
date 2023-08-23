from django.contrib import admin
from .models import SchemeProgress,QuizScore,StudentReport,AssignmentScore

admin.site.register(StudentReport)
admin.site.register(QuizScore)
admin.site.register(AssignmentScore)
admin.site.register(SchemeProgress)
