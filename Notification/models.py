from django.db import models
from Course.models import Course,Grade
from Log.models import Student

class Notification(models.Model):
    title = models.CharField(max_length=50, blank=True)
    TYPE = (
        ('quiz', 'quiz'),
        ('assingment', 'assignmnet'),
        ('scheme', 'scheme'),
        ('timetable', 'timetable')
    )
    type = models.CharField(max_length=100, choices=TYPE, default='assignment')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  
    con = models.CharField(max_length=5000)
    date_published = models.DateTimeField(auto_now_add=True)
    link_slug = models.CharField(max_length=300, blank=True)
    def save(self, *args , **kwargs):
        if not self.title:
            self.title = self.con[:20]
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.title} {self.grade}'

class NotificationStatus(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    note_json = models.JSONField(default=list, blank=True)
    counter = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Notification Statuses'
    def __str__(self):
        return f'{self.student} note_progress'
