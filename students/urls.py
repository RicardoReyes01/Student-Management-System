from django.urls import path
from . import views
from calendar_app import views as calendar_views

urlpatterns = [path('', views.index, name='index'),
               path('<int:id>', views.view_student, name='view_student'),
               path('add/', views.add, name='add'),
               path('edit/<int:id>', views.edit, name='edit'),
               path('delete/<int:id>', views.delete, name='delete'),
               path('search/', views.search_students, name='search_students'),
               path('calendar', views.calendar_view, name='calendar')]