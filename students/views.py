from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
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
    month = datetime.now().month
    year = datetime.now().year
    cal = calendar.HTMLCalendar().formatmonth(year, month)
    
    if request.method == 'POST':
        # Process form submission
        event_date = request.POST.get('event-date')
        event_name = request.POST.get('event-name')
        
        # Create and save the CalendarEvent instance
        CalendarEvent.objects.create(date=event_date, name=event_name)
        
        # Redirect to the calendar page or any other appropriate page
        return redirect('calendar')
    
    # If request method is not POST or if it's a GET request, render the calendar page
    events = CalendarEvent.objects.all()
    return render(request, 'calendar.html', {'events': events, 'calendar': cal})

def view_event(request):
    events = CalendarEvent.objects.all()
    return render(request, 'view_events.html', {'events': events})

from django.shortcuts import redirect
from django.contrib import messages

def delete_events(request):
    if request.method == 'POST':
        selected_events_data = request.POST.getlist('selected_events')
        for event_data in selected_events_data:
            event_id, event_date = event_data.split('|')  # Splitting the combined value
            try:
                # Validate date format
                parsed_date = parse_date(event_date)
                if parsed_date is None:
                    raise ValidationError('Invalid date format. Must be in YYYY-MM-DD format.')

                # Process deletion
                CalendarEvent.objects.filter(id=event_id).delete()
                # Optionally, delete additional data related to the event

            except ValidationError as e:
                # Handle validation error
                messages.error(request, e.message)

        return redirect('calendar')
    else:
        # Handle GET request if needed
        pass

