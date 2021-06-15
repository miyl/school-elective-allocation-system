from django.db import models

TYPES = ((0, "needs to have m out of n courses"), (1, "number of courses"),
         (2, "needs to have course x, y, z"), (3, "shouldn't have course x, y, z"),
         (4, "max m out of n courses"))

class Student(models.Model):
  first_name = models.CharField(max_length=200)
  email_address = models.CharField(max_length=75)
  login_code = models.CharField(max_length=75, null=True, blank=True)

  assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

  unique_together = ["assignment", "email_address"]

  def __str__(self):
    return self.first_name

  class Meta:
    ordering = ['first_name']

class Teacher(models.Model):
  full_name = models.CharField(max_length=200)

  # When adding a teacher, it's from the list of teachers from the school
  school = models.ForeignKey('School', on_delete=models.CASCADE)
  # When listing teachers teaching a course
  courses = models.ManyToManyField('Course', blank=True)

  def __str__(self):
    return self.full_name

  class Meta:
    ordering = ['full_name']

class Course(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  active = models.BooleanField(default=True)
  max_capacity = models.PositiveSmallIntegerField(null=True, blank=True)

  assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Student_Course_Association(models.Model):
  priority = models.PositiveSmallIntegerField()

  course = models.ForeignKey('Course', on_delete=models.CASCADE)
  student = models.ForeignKey('Student', on_delete=models.CASCADE)
  assigned = models.BooleanField(default=False)

  class Meta:
    verbose_name='Student Course Association'
    ordering = ['-priority']

  def __str__(self):
    return str(self.student) + " - " + str(self.course) + ": " + str(self.priority)

class Criterion(models.Model):
  type = models.PositiveSmallIntegerField(choices=TYPES)
  all = models.BooleanField(default=False)

  # Skal laves til many to many
  courses = models.ManyToManyField('Course', blank=True)
  students = models.ManyToManyField('Student', blank=True)
  assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)

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
  results_email = models.TextField(null=True, blank=True )
  priority_form_text = models.TextField(null=True, blank=True)

  invitation_email_sent = models.BooleanField(default=False)
  reminder_email_sent = models.BooleanField(default=False)
  results_email_sent = models.BooleanField(default=False)

  deadline = models.DateField(null=True, blank=True)
  school = models.ForeignKey('School', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
