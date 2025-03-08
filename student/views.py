from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Attendance, Course, Section, StudentProgress, AcademicScore, Task
from datetime import date, timedelta
import calendar
from django.contrib.auth.models import User
import random

# Create your views here.

# def index (request):
#     return render(request, 'student_app/index.html')


def index(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    return render(request, 'student_app/index.html', {'profile': profile})

# ---------------------------------------------------------------------

# def student_details(request):
#     if request.user.is_authenticated:
#         try:
#             profile = Profile.objects.get(user=request.user)
#             return {
#                 'student': {
#                     'name': profile.user.get_full_name(),
#                     'roll_no': profile.roll_no,
#                     'std': profile.std,
#                     'division': profile.division,
#                 }
#             }
#         except Profile.DoesNotExist:
#             return {'student': None}
#     return {'student': None}

# @login_required
# def dashboard_view(request):
#     # Fetch the logged-in user's profile
#     profile = None
#     if request.user.is_authenticated:
#         try:
#             profile = Profile.objects.get(user=request.user)
#         except profile.DoesNotExist:
#             profile = None  # Handle if profile doesn't exist
    
#     student = request.user
#     today = date.today()
#     year, month = today.year, today.month

#     # Get all attendance records for the current month
#     attendance_records = Attendance.objects.filter(
#         student=student, 
#         date__year=year, 
#         date__month=month
#     )
    
#     # Create a dictionary to map dates to attendance status
#     attendance_dict = {record.date: record.status for record in attendance_records}

#     # Count attendance statuses
#     total_days = calendar.monthrange(year, month)[1]  # Total days in the month
#     present_count = attendance_records.filter(status='Present').count()
#     absent_count = attendance_records.filter(status='Absent').count()
#     late_count = attendance_records.filter(status='Late').count()
#     total_records = present_count + absent_count + late_count

#     # Attendance percentage calculation
#     if total_records > 0:
#         attendance_percentage = (present_count / total_records) * 100
#     else:
#         attendance_percentage = 0

#     # Generate the calendar for the current month
#     cal = calendar.Calendar()
#     days = cal.itermonthdays4(year, month)  # Returns (year, month, day, weekday)

#     # Create a list of day objects with attendance status
#     calendar_days = []
#     for y, m, d, wd in days:
#         if m == month:  # Include only the current month's days
#             date_obj = date(y, m, d)
#             status = attendance_dict.get(date_obj, 'No Record')
#             calendar_days.append({
#                 'date': date_obj,
#                 'day': d,
#                 'weekday': calendar.day_name[wd],
#                 'status': status,
#             })

#     context = {
#         'profile': profile,
#         'welcome_message': f"Welcome, {request.user.username}!",
#         'calendar_days': calendar_days,
#         'month': today.strftime('%B %Y'),
#         'present_count': present_count,
#         'absent_count': absent_count,
#         'late_count': late_count,
#         'total_days': total_days,
#         'attendance_percentage': round(attendance_percentage, 2),
#     }

#     return render(request, 'student_app/dashboard.html', context)

def dashboard_view(request):
    # Fetch the logged-in user's profile
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Handle if profile doesn't exist
    else:
        profile = None
    
    student = request.user if request.user.is_authenticated else None
    today = date.today()
    year, month = today.year, today.month

    # Only fetch attendance records if the user is authenticated
    attendance_records = Attendance.objects.filter(
        student=student, 
        date__year=year, 
        date__month=month
    ) if student else []

    # Create a dictionary to map dates to attendance status
    attendance_dict = {record.date: record.status for record in attendance_records}

    # Count attendance statuses
    total_days = calendar.monthrange(year, month)[1]  # Total days in the month
    present_count = sum(1 for record in attendance_records if record.status == 'Present')
    absent_count = sum(1 for record in attendance_records if record.status == 'Absent')
    late_count = sum(1 for record in attendance_records if record.status == 'Late')
    total_records = present_count + absent_count + late_count

    # Attendance percentage calculation
    if total_records > 0:
        attendance_percentage = (present_count / total_records) * 100
    else:
        attendance_percentage = 0

    # Generate the calendar for the current month
    cal = calendar.Calendar()
    days = cal.itermonthdays4(year, month)  # Returns (year, month, day, weekday)

    # Create a list of day objects with attendance status
    calendar_days = []
    for y, m, d, wd in days:
        if m == month:  # Include only the current month's days
            date_obj = date(y, m, d)
            status = attendance_dict.get(date_obj, 'No Record')
            calendar_days.append({
                'date': date_obj,
                'day': d,
                'weekday': calendar.day_name[wd],
                'status': status,
            })

    context = {
        'profile': profile,
        'welcome_message': f"Welcome, {request.user.username}!" if request.user.is_authenticated else "Welcome, Guest!",
        'calendar_days': calendar_days,
        'month': today.strftime('%B %Y'),
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'total_days': total_days,
        'attendance_percentage': round(attendance_percentage, 2),
    }

    return render(request, 'student_app/dashboard.html', context)

# @login_required
# def courses_view(request):
#     student = request.user
#     progress_list = []

#     # Get all courses and their progress for the student
#     courses = Course.objects.all()
#     for course in courses:
#         progress, created = StudentProgress.objects.get_or_create(student=student, course=course)
#         progress_list.append({
#             'course': course,
#             'completion_percentage': round(progress.course_completion_percentage, 2),
#         })
    
#     context = {
#         'progress_list':progress_list
#     }

#     return render(request, 'student_app/courses.html', context)

def courses_view(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    progress_list = []

    courses = Course.objects.all()  # Fetch all courses

    if request.user.is_authenticated:
        student = request.user
        for course in courses:
            progress, created = StudentProgress.objects.get_or_create(student=student, course=course)
            progress_list.append({
                'course': course,
                'completion_percentage': round(progress.course_completion_percentage, 2),
            })
    else:
        # If user is not logged in, just show courses without progress
        progress_list = [{'course': course, 'completion_percentage': None} for course in courses]

    context = {'progress_list': progress_list, 'profile':profile}
    return render(request, 'student_app/courses.html', context)

@login_required
def course_detail_view(request, course_id):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    # Fetch the course and student's progress
    course = get_object_or_404(Course, id=course_id)
    student = request.user
    progress, created = StudentProgress.objects.get_or_create(student=student, course=course)
    sections = course.sections.all()

    if request.method == 'POST':
        # Handle marking a section as completed
        if 'section_id' in request.POST:
            section_id = request.POST.get('section_id')
            section = get_object_or_404(Section, id=section_id)

            if 'reset_section' in request.POST:  # Handle resetting the section
                progress.completed_sections.remove(section)
            else:  # Mark the section as completed
                progress.completed_sections.add(section)

        # Save progress after modification
        progress.save()

        # Redirect to the same page
        return redirect('course_detail', course_id=course_id)

    context = {
        'course': course,
        'sections': sections,
        'progress': progress,
        'profile':profile,
    }
    return render(request, 'student_app/course_detail.html', context)

# @login_required    
# def academic_scores(request):
#     student_profile = get_object_or_404(User, first_name=request.user.first_name)
#     scores = AcademicScore.objects.filter(student_profile = student_profile)

#     # Calculate overall Percentage
#     total_score = sum([s.scores for s in scores])
#     num_courses = scores.count()
#     overall_percentage = (total_score / (num_courses * 100)) * 100 if num_courses > 0 else 0

#     # Determine final grade and remarks based on average score
#     def overall_grade(percentage):
#         if percentage >= 90:
#             return 'A+'
#         elif percentage >= 80:
#             return 'A'
#         elif percentage >= 70:
#             return 'B'
#         elif percentage >= 60:
#             return 'C'
#         elif percentage >= 50:
#             return 'D'
#         else:
#             return 'F'
        
#     def overall_remarks(grade):
#         remarks_dict = {
#             'A+': 'Outstanding Performance!',
#             'A': 'Great Job! Keep pushing.',
#             'B': 'Good! Keep improving.',
#             'C': 'Fair Performance.',
#             'D': 'Below Average. Work harder!',
#             'F': 'Failed. You need more effort!',
#         }
#         return remarks_dict.get(grade, 'No remarks')
    
#     final_grade = overall_grade(overall_percentage)
#     final_remarks = overall_remarks(final_grade)

#     context = {
#         'student_profile': student_profile,
#         'scores': scores,
#         'overall_percentage': overall_percentage,
#         'final_grade': final_grade,
#         'final_remarks': final_remarks,
#     }

#     return render(request, 'student_app/academic_scores.html', context)

def academic_scores(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    courses = Course.objects.all()  # Fetch all courses

    if request.user.is_authenticated:
        student_profile = get_object_or_404(User, first_name=request.user.first_name)
        scores = AcademicScore.objects.filter(student_profile=student_profile)

        # Calculate overall Percentage
        total_score = sum([s.scores for s in scores])
        num_courses = scores.count()
        overall_percentage = (total_score / (num_courses * 100)) * 100 if num_courses > 0 else 0

        # Determine final grade and remarks based on average score
        def overall_grade(percentage):
            if percentage >= 90:
                return 'A+'
            elif percentage >= 80:
                return 'A'
            elif percentage >= 70:
                return 'B'
            elif percentage >= 60:
                return 'C'
            elif percentage >= 50:
                return 'D'
            else:
                return 'F'
            
        def overall_remarks(grade):
            remarks_dict = {
                'A+': 'Outstanding Performance!',
                'A': 'Great Job! Keep pushing.',
                'B': 'Good! Keep improving.',
                'C': 'Fair Performance.',
                'D': 'Below Average. Work harder!',
                'F': 'Failed. You need more effort!',
            }
            return remarks_dict.get(grade, 'No remarks')
        
        final_grade = overall_grade(overall_percentage)
        final_remarks = overall_remarks(final_grade)

        context = {
            'is_authenticated': True,
            'student_profile': student_profile,
            'courses': courses,
            'scores': scores,
            'overall_percentage': overall_percentage,
            'final_grade': final_grade,
            'final_remarks': final_remarks,
            'profile':profile,
        }
    else:
        context = {
            'is_authenticated': False,
            'courses': courses,
            'profile':profile,
        }

    return render(request, 'student_app/academic_scores.html', context)

# ------------------------------------------------------------------------------------------------------------

# List of motivational quotes
QUOTES = [
    "Believe in yourself! You can do it. 💪",
    "Every task completed brings you closer to success. 🚀",
    "Focus on progress, not perfection. 🌱",
    "The secret to success is to start. 🏆",
    "You are capable of amazing things! 💡"
]

def task_list(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    tasks = Task.objects.all().order_by('-created_at')
    quote = random.choice(QUOTES)  # Random quote for motivation

    context = { 
        'tasks':tasks,
        'quote':quote,
        'profile':profile,
    }

    return render(request, 'student_app/task_list.html', context)

# Create a New Task
def create_task(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'Medium')
        progress = request.POST.get('progress', 'Not Started')

        Task.objects.create(
            title = title,
            description = description,
            priority=priority,
            progress=progress,
        )

        return redirect(task_list)

    context = {
        'profile':profile,
    }

    return render(request, 'student_app/create_task.html', context)

# ---------------------------------------------------------------------------------------

# Update a Task
def update_task(request, task_id):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority', task.priority)
        task.progress = request.POST.get('progress', task.progress)
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')
    
    context = {
        'task':task,
        'profile':profile,
    } 

    return render(request, 'student_app/update_task.html', context)

# ------------------------------------------------------------------------------------------

# Delete a Task

def delete_task(request, task_id):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'student_app/delete_task.html', {'task': task, 'profile':profile})