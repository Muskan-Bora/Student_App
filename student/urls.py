from django.urls import path, include
from student import views

# app_name = 'student'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('courses_list/', views.courses_view, name='courses_list'),
    path('<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('scores/', views.academic_scores, name='academic_scores'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]