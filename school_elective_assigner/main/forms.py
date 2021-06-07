from django.forms import ModelForm, ChoiceField, HiddenInput
from .models import (Assignment, Student, Course, Student_Course_Request,
     Student_Course_Assignment, Teacher, Criterion)

# We want django admin's ManyToMany boxes instead of django's default
from django.contrib.admin.widgets import FilteredSelectMultiple

class StudentForm(ModelForm):
  class Meta:
    model = Student
    exclude = ('login_code', )
    # Assignment should be hidden plz
    widgets = {'assignment': HiddenInput()}

class CriterionForm(ModelForm):
  class Meta:
    model = Criterion
    exclude = ('assignment', )
    #students = ChoiceField(widget=FilteredSelectMultiple)
    #filter_horizontal = ('students',)
    widgets = {'students': FilteredSelectMultiple("abc", True), 'courses':
        FilteredSelectMultiple("abc", True)}
    #fields = '__all__'

class CourseForm(ModelForm): 
  class Meta: 
    model = Course
    exclude = ( 'active', )