from django.db import models

class Student(models.Model):
  first_name = models.CharField(max_length=200)
  email_address = models.CharField(max_length=75)
  login_code = models.CharField(max_length=75, null=True, blank=True)

  assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

  unique_together = ["assignment", "email_address"]

  def __str__(self):
    return self.first_name

class Teacher(models.Model):
  full_name = models.CharField(max_length=200)

  school = models.ForeignKey('School', on_delete=models.CASCADE)

  def __str__(self):
    return self.full_name

class Course(models.Model):
  name_en = models.CharField(max_length=200)
  name_da = models.CharField(max_length=200)
  description_en = models.TextField()
  description_da = models.TextField()
  active = models.BooleanField(default=True)
  deadline = models.DateField()

  assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

  def __str__(self):
    return self.name_da

class Student_Course_Request(models.Model):
  priority = models.PositiveSmallIntegerField()

  course = models.ForeignKey('Course', on_delete=models.CASCADE)
  student = models.ForeignKey('Student', on_delete=models.CASCADE)

  class Meta:
    verbose_name='Student Course Request'

  def __str__(self):
    return f"self.student (self.course): self.priority"

# Only has foreign keys
class Student_Course_Assignment(models.Model):
  course = models.ForeignKey('Course', on_delete=models.CASCADE)
  student = models.ForeignKey('Student', on_delete=models.CASCADE)

  class Meta:
    verbose_name='Student Course Assignment'

  def __str__(self):
    return f"self.student (self.course)"

class Criterion(models.Model):
  name = models.CharField(max_length=200)
  type = models.PositiveSmallIntegerField()

  course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
  student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural='criteria'

class School(models.Model):
  email_address = models.CharField(max_length=200, primary_key=True)
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

  school = models.ForeignKey('School', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
