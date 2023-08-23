from django.db import models
from Course.models import Grade
from django.utils import timezone
from django.utils.text import slugify

class Event(models.Model):
    name = models.CharField(max_length=300)
    grade = models.ManyToManyField(Grade)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    color = models.CharField(max_length=300, default='salmon')
    slug = models.SlugField(max_length=300, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args , **kwargs)
    def __str__(self):
        return self.name

class Notice(models.Model):
    name = models.CharField(max_length=300)
    grade = models.ManyToManyField(Grade)
    image = models.ImageField(default='default.jpg', upload_to='notice')
    content = models.TextField(max_length=3000)
    published = models.DateField(auto_now_add=True)
    end_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args , **kwargs)
    def __str__(self):
        return self.name

class Grading(models.Model):
    grade = models.CharField(max_length=50)
    min_mark = models.IntegerField()
    max_mark = models.IntegerField()
    remark = models.CharField(max_length=100, null=True, blank=True)
    color_code = models.CharField(max_length=300, default='salmon')
    def __str__(self):
        return f'{self.grade} | {self.min_mark} - {self.max_mark}'
    

class TimeTableTemplate(models.Model):
    name = models.CharField(max_length=200, default='default timetable template')
    headers = models.JSONField(default=list)
    con = models.JSONField(default=list)
    def __str__(self):
        return self.name
    
class TimeTable(models.Model):
    grade = models.OneToOneField(Grade, on_delete=models.CASCADE)
    headers = models.JSONField(default=list) 
    con = models.JSONField(default=list)
    def __str__(self):
        return f'{self.grade} time table'