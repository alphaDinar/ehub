from django.db import models
from django.utils.text import slugify
from Log.models import Student
from Quiz.models import Quiz,Assignment
from Course.models import Course
from Scheme.models import Scheme
    

class SchemeProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    progress_json = models.JSONField(blank=True,null=True)
    progress_count = models.FloatField(default=0)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.student}"s {self.scheme} progress'
    class Meta:
        verbose_name_plural = 'SchemeProgresses'

class StudentReport(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    report = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f'{self.student}"s Report'

class QuizScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    holder = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    con = models.JSONField(blank=True,null=True) 
    ans_box = models.JSONField(blank=True,null=True) 
    mark = models.FloatField()
    choice_box = models.JSONField(blank=True,null=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f'{self.student.name}   {self.holder.title} {self.mark}'

class AssignmentScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    holder = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    con = models.JSONField(blank=True,null=True) 
    ans_box = models.JSONField(blank=True,null=True) 
    mark = models.FloatField()
    choice_box = models.JSONField(blank=True,null=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f'{self.student.name}   {self.holder.title} {self.mark}'

