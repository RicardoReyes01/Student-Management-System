from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
import calendar
from datetime import datetime

from .models import Student
from .models import CalendarEvent
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

def edit(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/edit.html', {
                'form': form, 
                'success': True
            })
    else:
        student = Student.objects.get(pk=id)
        form = StudentForm(instance=student)
    return render(request, 'students/edit.html', {'form': form})

def delete(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))   

def search_students(request):
    query = request.GET.get('query').strip()
    search_results = []  # Initialize an empty list
    if query:
        search_results = Student.objects.filter(first_name__icontains=query) | Student.objects.filter(last_name__icontains=query)
        print("Search Query: ", query)
        print("Search Results: ", search_results)
    return render(request, 'students/search_students.html', {'search_students': search_results, 'query': query})

def calendar_view(request):
    # Assuming you have a model named CalendarEvent to store events
    events = CalendarEvent.objects.all()
    return render(request, 'calendar.html', {'events': events})

        
        
