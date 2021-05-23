from django.db import models

class Student(models.Model):
  first_name = models.CharField(max_length=200)
  login_code = models.CharField(max_length=75, null=True, blank=True)
  #imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

  def __str__(self):
    return self.first_name

class Teacher(models.Model):
  full_name = models.CharField(max_length=200)

  def __str__(self):
    return self.full_name

class Course(models.Model):
  name_en = models.CharField(max_length=200)
  name_da = models.CharField(max_length=200)
  description_en = models.TextField()
  description_da = models.TextField()
  active = models.BooleanField(default=True)
  deadline = models.DateField()

  def __str__(self):
    return self.name_da

class Student_Course_Request(models.Model):
  priority = models.PositiveSmallIntegerField()

  def __str__(self):
    return self.priority

# Only has foreign keys
class Student_Course_Assigned(models.Model):
  pass

  #def __str__(self):
  #  return self.name

class Rule(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class School(models.Model):
  name = models.CharField(max_length=100)
  password = models.CharField(max_length=200)
  logo = models.FileField(upload_to="uploads/logos", null=True, blank=True)
  email_footer = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.name

class Assignment(models.Model):
  name = models.CharField(max_length=200)
  invitation_email = models.TextField(max_length=200, null=True, blank=True)
  reminder_email = models.TextField(null=True, blank=True )
  priority_form_text = models.TextField(null=True, blank=True)
  emails_sent = models.BooleanField(default=False)

  def __str__(self):
    return self.name
