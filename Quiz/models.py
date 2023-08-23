from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from Log.models import User, Teacher
from Course.models import Course
from Scheme.models import Scheme

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    duration = models.IntegerField(help_text='Duration allowed for Quiz in minutes', default=60)
    con = models.JSONField(default=list)
    marking_scheme = models.JSONField(default=list)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    def get_quiz_scores(self):
        return self.quizscore_set.all()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'quizes'

class Assignment(models.Model):
    STATUS = (
        ('pending','pending'),
        ('completed','completed')
    )
    PROTECTION = (
        ('locked', 'locked'),
        ('unlocked', 'unlocked')
    )
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    deadline = models.DateTimeField(default=timezone.now)
    con = models.JSONField(default=list)
    marking_scheme = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    protection = models.CharField(max_length=50, choices=PROTECTION, default='locked')
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    def get_assignment_scores(self):
        return self.assignmentscore_set.all()
    def __str__(self):
        return self.title

class AssignmentSession(models.Model):
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)
    time = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f'{self.assignment} session'

