from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.utils import timezone
from Log.models import Teacher
from Course.models import Grade,Course
from cloudinary.models import CloudinaryField
import datetime

choice = (
    ('pending','pending'),
    ('active','active'),
    ('completed','completed'),
)


class Scheme(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    status = models.CharField(max_length=30, choices=choice, default='pending')
    time_started = models.DateField(null=True,blank=True)
    time_completed = models.DateField(null=True,blank=True)
    date_created = models.DateField(auto_now_add=True)
    # last_touched = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = slugify(self.topic)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.course}  - {self.topic}"
    def get_images(self):
        return self.image_set.all()
    def get_videos(self):
        return self.video_set.all()
    def get_passages(self):
        return self.passage_set.all()
    def get_pdfs(self):
        return self.pdf_set.all()
    def get_slides(self):
        return self.slide_set.all()
    def get_quizes(self):
        return self.quiz_set.all()
    def get_assignments(self):
        return self.assignment_set.order_by('deadline')
        
    def get_scores(self):
        return self.score_set.all()

class RecentScheme(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.teacher} {self.scheme}'

class Image(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(default='default.jpg',upload_to='Scheme_images')
    # image = CloudinaryField("Image" ,folder='TM/Scheme_image', resource_type='auto')
    holder = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Passage(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(max_length=10000)
    thumb = models.ImageField(default='Scheme_images/google-document-icon-free-png_r0pGceu.png',upload_to='Scheme_images',blank=True,null=True)
    # thumb = CloudinaryField("Image" ,folder='TM/Scheme_image', resource_type='auto', default='https://res.cloudinary.com/dvnemzw0z/image/upload/v1683386036/5064889_wpiq8e.png')
    holder = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Video(models.Model):
    name = models.CharField(max_length=300)
    video = models.FileField(default='vid.jpg', upload_to='TM/Scheme_video', validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    # video = CloudinaryField("Video" ,folder='TM/Scheme_video', resource_type='auto')
    holder = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Pdf(models.Model):
    name = models.CharField(max_length=300)    
    pdf = models.FileField(default='vid.jpg', upload_to='TM/Scheme_doc', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    # pdf = CloudinaryField("Video" ,folder='TM/Scheme_video', resource_type='auto')
    holder = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Slide(models.Model):
    title = models.CharField(max_length=300)
    con = models.JSONField()
    holder = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Reference(models.Model):
    name = models.CharField(max_length=300)
    link = models.CharField(max_length=3000)

#change slide to links and text reference... 

# class PastResources(models.Model):

class Meeting(models.Model):
    token = models.CharField(max_length=3000)
    meeting_id = models.CharField(max_length=3000)
    passcode = models.CharField(max_length=1000)
    topic = models.CharField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    duration = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    join_url = models.CharField(max_length=3000)
    def __str__(self):
        return self.topic