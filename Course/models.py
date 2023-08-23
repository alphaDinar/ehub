from django.db import models
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Grade(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=100)
    slug = models.SlugField(max_length=400, null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self):
        return f'{self.name}'
    def get_courses(self):
        return self.course_set.all()
    def get_students(self):
        return self.student_set.all()
    def get_meetings(self):
        return self.meeting_set.all()

class Course(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300) 
    abb = models.CharField(max_length=10)
    slug = models.SlugField(blank=True,null=True)
    def save(self, *args, **kwargs):
        self.abb = self.subject[:3].upper()
        self.slug = slugify(self.abb) + slugify(self.grade.code)
        super().save(*args, **kwargs)
    def get_schemes(self):
        return self.scheme_set.all() 
    def get_scheme_progress(self):
        return self.schemeprogress_set.all()
    def get_quizes(self):
        return self.quiz_set.all()
    def get_quiz_scores(self):
        return self.quiz_score_set.all()
    def get_assignments(self):
        return self.assignment_set.all()
    def get_meetings(self):
        return self.meeting_set.all()
    def __str__(self):
        return f'{self.abb} {self.grade.code}'   
     
    
# class CourseReview(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     review = models.TextField(max_length=3000)
#     ratings = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
#     date_posted = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField()
#     def __str__(self):
#         return self.slug[:30]