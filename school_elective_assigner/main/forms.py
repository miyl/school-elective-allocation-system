from django.forms import ModelForm
from .models import (Assignment, Student, Course, Student_Course_Request,
     Student_Course_Assignment, Teacher, Criterion)

class StudentForm(ModelForm):
  class Meta:
    model = Student
    exclude = ('login_code', )

class CriterionForm(ModelForm):
  class Meta:
    model = Criterion
    fields = '__all__'
    #exclude = ('login_code', )
