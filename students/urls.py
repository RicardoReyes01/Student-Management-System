from django.urls import path, include
from . import views

urlpatterns = [path('', views.index, name='index'),
               path('<int:id>', views.view_student, name='view_student'),
               path('add/', views.add, name='add'),
               path('edit/<int:id>', views.edit, name='edit'),
               path('delete/<int:id>', views.delete, name='delete'),
               path('search/', views.search_students, name='search_students'),
               path('calendar', views.calendar_view, name='calendar'),
               path('view-events/', views.view_event, name='view_events'),
               path('delete-events/', views.delete_events, name='delete_events'),
               path('announcements/', views.current_announcements, name='announcements_list'),
               path('grades/', views.grades, name='grades'),
               ]