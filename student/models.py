from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default="Date")
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent'),
            ('Late', 'Late'),
        ],
        default='Present'
    )

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"
    
class Course(models.Model):
    name = models.CharField(max_length=200, default='Name of the Course')
    description = models.TextField()

    def __str__(self):
        return self.name

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()  # Order of the section in the course

    def __str__(self):
        return f"{self.name} ({self.course.name})"
    
class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_sections = models.ManyToManyField(Section, blank=True)

    @property
    def course_completion_percentage(self):
        total_sections = self.course.sections.count()
        if total_sections == 0:
            return 0
        completed_count = self.completed_sections.count()
        return (completed_count / total_sections) * 100

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"
    
class AcademicScore(models.Model):
    student_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    scores = models.FloatField()

    def grade(self):
        """ Returns the grade based on the score """
        if self.score >= 90:
            return 'A+'
        elif self.score >= 80:
            return 'A'
        elif self.score >= 70:
            return 'B'
        elif self.score >= 60:
            return 'C'
        elif self.score >= 50:
            return 'D'
        else:
            return 'F'
        
    def remarks(self):
        """Returns remarks based on the grade"""
        grade = self.grade()
        remarks_dict = {
            'A+': 'Excellent! Keep it up.',
            'A': 'Very Good! Aim for A+.',
            'B': 'Good! You can do better.',
            'C': 'Fair! Need improvement.',
            'D': 'Needs more effort.',
            'F': 'Failed. Work harder!',
        }
        return remarks_dict.get(grade, 'No remarks')
    
    def __str__(self):
        return f"{self.student_profile} - {self.course.name} - {self.scores}"
    
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    PROGRESS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(
        max_length = 300,
        default = 'Enter some Title',
    )

    description = models.TextField(
        blank = True,
        null = True,
        default = 'Description',
    )

    completed = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='Not Started')

    def __str__(self):
        return self.title