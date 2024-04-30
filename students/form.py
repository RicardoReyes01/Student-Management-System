from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_number', 'first_name', 'last_name', 'email', 'major', 'gpa']
        labels = {
            'student_number': 'Student Number', 
            'first_name': 'First Name', 
            'last_name': 'Last Name', 
            'email': 'Email', 
            'major': 'Major', 
            'gpa': 'GPA'
        }
        
        widgets = {
            'student_number': forms.NumberInput(attrs={'class': 'form_control'}), 
            'first_name': forms.TextInput(attrs={'class': 'form_control'}), 
            'last_name': forms.TextInput(attrs={'class': 'form_control'}), 
            'email': forms.EmailInput(attrs={'class': 'form_control'}), 
            'major': forms.TextInput(attrs={'class': 'form_control'}), 
            'gpa': forms.NumberInput(attrs={'class': 'form_control'})
        }
        