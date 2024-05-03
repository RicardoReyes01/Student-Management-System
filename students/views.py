from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
import calendar
from datetime import datetime

from .models import Student
from students.models import Grade
from .models import CalendarEvent
from .forms import StudentForm, GradeForm
from .models import Announcement

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
            form.save() 
            return redirect('index') 
    else:
        form = StudentForm() 
        
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
    search_results = []
    if query:
        search_results = Student.objects.filter(first_name__icontains=query) | Student.objects.filter(last_name__icontains=query)
        print("Search Query: ", query)
        print("Search Results: ", search_results)
    return render(request, 'students/search_students.html', {'search_students': search_results, 'query': query})

def calendar_view(request):
    month = datetime.now().month
    year = datetime.now().year
    cal = calendar.HTMLCalendar().formatmonth(year, month)
    
    if request.method == 'POST':
        # Process form submission
        event_date = request.POST.get('event-date')
        event_name = request.POST.get('event-name')
        
        CalendarEvent.objects.create(date=event_date, name=event_name)
        
        return redirect('calendar')
    
    events = CalendarEvent.objects.all()
    return render(request, 'calendar.html', {'events': events, 'calendar': cal})

def view_event(request):
    events = CalendarEvent.objects.all()
    return render(request, 'view_events.html', {'events': events})

def delete_events(request):
    if request.method == 'POST':
        selected_events_data = request.POST.getlist('selected_events')
        for event_data in selected_events_data:
            event_id, event_date = event_data.split('|')
            try:
                parsed_date = parse_date(event_date)
                if parsed_date is None:
                    raise ValidationError('Invalid date format. Must be in YYYY-MM-DD format.')

                # Process deletion
                CalendarEvent.objects.filter(id=event_id).delete()

            except ValidationError as e:
                messages.error(request, e.message)

        return redirect('calendar')
    else:
        # Handle GET request if needed
        pass

def current_announcements(request):
    announcements = Announcement.objects.order_by('-date_posted')[:5] 
    return render(request, 'announcement.html', {'announcements': announcements})

def grades(request):
    grades = Grade.objects.select_related('student').all()
    return render(request, 'grades.html', {'grades': grades})

def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm()
    return render(request, 'add_grade.html', {'form': form})

def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'edit_grade.html', {'form': form})

def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grades')
    return render(request, 'delete_grade.html', {'grade': grade})