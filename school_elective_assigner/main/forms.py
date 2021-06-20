from django.contrib.admin import widgets
from django.forms import ModelForm, Form, ChoiceField, HiddenInput, FileField
from .models import (Assignment, Student, Course, Student_Course_Association,
     Teacher, Criterion)
from django.core.validators import FileExtensionValidator

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

class TeacherForm(ModelForm):
  class Meta:
    model = Teacher
    exclude = ( 'courses', )
    widgets = {'school': HiddenInput()}

class AssignmentForm(ModelForm):
  class Meta:
    model = Assignment
    exclude = ( 'invitation_email_message', 'invitation_email_subject', 'reminder_email_subject', 
                'reminder_email_message', 'results_email_subject', 'results_email_message',
                'priority_form_text', 'invitation_email_sent', 'reminder_email_sent',
                'results_email_sent', 'deadline')
    widgets = {'school': HiddenInput()}
    #fields = '__all__'

# Example of a Form without a model - boom!
class UploadStudentsCSVForm(Form):
  # TODO: This really should be validated further, to ensure it's a valid CSV file
  file = FileField(validators=[FileExtensionValidator(allowed_extensions=['csv'])])
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

class InvitationEmailForm(ModelForm):
  class Meta:
    model = Assignment
    exclude = ( 'name', 'results_email_message', 'results_email_subject',
                'reminder_email_subject', 'reminder_email_message', 'priority_form_text',
                'invitation_email_sent', 'reminder_email_sent', 'results_email_sent',
                'deadline', 'school', )
    

class ReminderEmailForm(ModelForm):
  class Meta:
    model = Assignment
    exclude = ( 'name', 'results_email_message', 'results_email_subject',
                'priority_form_text', 'invitation_email_sent',
                'reminder_email_sent', 'results_email_sent',
                'deadline', 'school', 'invitation_email_subject',
                'invitation_email_message', )
    
class ResultEmailForm(ModelForm):
  class Meta:
    model = Assignment
    exclude = ( 'name', 'priority_form_text', 'invitation_email_sent',
                'reminder_email_sent', 'results_email_sent',
                'deadline', 'school', 'invitation_email_subject',
                'invitation_email_message', 'reminder_email_subject',
                'reminder_email_message', )

class EditDeadlineForm(ModelForm):
  class Meta:
    model = Assignment
    exclude = ( 'name', 'priority_form_text', 'invitation_email_sent',
                'reminder_email_sent', 'results_email_sent',
                'school', 'invitation_email_subject', 'results_email_message',
                'invitation_email_message', 'reminder_email_subject',
                'reminder_email_message', 'results_email_subject' )