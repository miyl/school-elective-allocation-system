from django.contrib import admin
from .models import (
  Student, Teacher, Course, Student_Course_Association,
  Criterion, School, Assignment)

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'email_address', 'assignment')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
  list_display = ('full_name', 'school')
  pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ('name', 'max_capacity', 'active', 'assignment')

@admin.register(Student_Course_Association)
class Student_Course_AssignmentAdmin(admin.ModelAdmin):
  list_display = ('student', 'priority', 'course', 'assigned')
  ordering = ('student',)

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
  list_display = ('name', 'type', 'all', 'm', 'n')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
  pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  pass