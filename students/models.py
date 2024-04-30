from django.db import models
import random, string

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
    
    def save(self, *args, **kwargs):
        if not self.student_number:
            self.student_number = self.generate_student_number()
        super().save(*args, **kwargs)
    
    def generate_student_number(self):
        # Generate a random 5-digit number
        return ''.join(random.choices(string.digits, k=5))