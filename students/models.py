from django.db import models

# Create your models here.
class Student(models.Model):
    student_number = models.CharField(max_length=5, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    major = models.CharField(max_length=50)
    gpa = models.FloatField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class CalendarEvent(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name   