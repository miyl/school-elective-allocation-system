from django.contrib import admin
from .models import (
  Student, Teacher, Course, Student_Course_Association,
  Criterion, School, Assignment)

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  pass

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
  pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  pass

@admin.register(Student_Course_Association)
class Student_Course_AssignmentAdmin(admin.ModelAdmin):
  list_display = ('student', 'priority', 'course', 'assigned')
  ordering = ('student',)

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
  pass

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
  pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  pass
