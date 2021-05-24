from django.contrib import admin
from .models import (
  Student, Teacher, Course, Student_Course_Request,
  Student_Course_Assignment, Criterion, School, Assignment)

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

@admin.register(Student_Course_Request)
class Student_Course_RequestAdmin(admin.ModelAdmin):
  pass

@admin.register(Student_Course_Assignment)
class Student_Course_AssignmentAdmin(admin.ModelAdmin):
  pass

@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
  pass

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
  pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  pass
