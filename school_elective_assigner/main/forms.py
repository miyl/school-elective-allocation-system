from django.forms import ModelForm, ChoiceField
from .models import (Assignment, Student, Course, Student_Course_Request,
     Student_Course_Assignment, Teacher, Criterion)

# We want django admin's ManyToMany boxes instead of django's default
from django.contrib.admin.widgets import FilteredSelectMultiple

class StudentForm(ModelForm):
  class Meta:
    model = Student
    exclude = ('login_code', )

class CriterionForm(ModelForm):
  class Meta:
    model = Criterion
    exclude = ('assignment', )
    #students = ChoiceField(widget=FilteredSelectMultiple)
    filter_horizontal = ('students',)
    #fields = '__all__'
