from django.contrib import admin
from student.models import Attendance
from student.models import Course
from student.models import Section
from student.models import StudentProgress
from student.models import AcademicScore
from student.models import Task

# Register your models here.
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('student', 'date', 'status')

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(StudentProgress)
admin.site.register(AcademicScore)
admin.site.register(Task)