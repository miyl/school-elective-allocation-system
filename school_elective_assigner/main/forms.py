from django.contrib.admin import widgets
from django.forms import ModelForm, Form, ChoiceField, HiddenInput, FileField
from .models import (Assignment, Student, Course, Student_Course_Association,
     Teacher, Criterion)

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
    #exclude = ('assignment', )
    #students = ChoiceField(widget=FilteredSelectMultiple)
    #filter_horizontal = ('students',)
    widgets = {'students': FilteredSelectMultiple("abc", True), 'courses':
        FilteredSelectMultiple("abc", True), 'assignment': HiddenInput()}
    fields = '__all__'

class CourseForm(ModelForm):
  class Meta:
    model = Course
    exclude = ( 'active', )
    widgets = {'assignment': HiddenInput()}

class AssignmentForm(ModelForm):
  class Meta:
    model = Assignment
    exclude = ( 'invitation_email', 'reminder_email', 'results_email',
                'priority_form_text', 'invitation_email_sent', 'reminder_email_sent',
                'results_email_sent', 'deadline')
    widgets = {'school': HiddenInput()}
    #fields = '__all__'

# Example of a Form without a model - boom!
class UploadStudentsCSVForm(Form):
  file = FileField()
  #class Meta:
    #widgets = {'assignment': HiddenInput()}
    #model = Assignment
    #fields = '__all__'

class DistributeStudentsForm(Form):
  pass
  #class Meta:
    #widgets = {'assignment': HiddenInput()}
    #model = Assignment
    #fields = '__all__'
