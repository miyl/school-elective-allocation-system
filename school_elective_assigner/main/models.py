from django.db import models


class Student(models.Model):
  first_name = models.CharField(max_length=200)
  login_code = models.CharField(max_length=75, null=True)
  #imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

class Teacher(models.Model):
  full_name = models.CharField(max_length=200)

class Course(models.Model):
  title = models.CharField(max_length=200)

class Student_Course_Request(models.Model):
  priority = models.

#
class Student_Course_Assigned(models.Model):
  pass

class Rules(models.Model):
  title = models.CharField(max_length=200)

class School(models.Model):
  title = models.CharField(max_length=200)
  j
class Assignment(models.Model):
  title = models.CharField(max_length=200)
