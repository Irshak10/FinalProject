from django.db import models

# Create your models here.


class Course(models.Model):
    course_name = models.TextField(default='', null=True)
