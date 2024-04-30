from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

from .models import Student
from .forms import StudentForm

# Create your views here.
def index(request):
    return render(
        request, 'index.html',
        {
            'students': Student.objects.all()
        })
    
def view_student(request, id):
    student = Student.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create a new student
            return redirect('index')  # Redirect to the index page after successful form submission
    else:
        form = StudentForm()  # Create a new form instance if it's a GET request
        
    return render(request, 'students/add.html', {'form': form})