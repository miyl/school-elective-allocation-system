from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import (Assignment, Student, Course,
     Student_Course_Association, Teacher, Criterion)
from .forms import ( StudentForm, CriterionForm, CourseForm, AssignmentForm,
  UploadStudentsCSVForm )
from ortools.linear_solver import pywraplp
from .forms import EmailForm, StudentForm, CriterionForm, CourseForm, AssignmentForm, EmailForm
from django.conf import settings
from django.core.mail import send_mail

def index(request):
  context = {}
  return render(request, 'index.html', context)


def assignments(request):
  # TODO: This is all assignments, not all assignments for the current
  # user/school which it should be
  assignments = Assignment.objects.all()

  progresses = []
  for asn in assignments:
    # If results e-mail has been sent there's no need for the subsequent
    # calculations?
    progress = 0
    if asn.results_email_sent:
      progress = 100
    else:
      if Student.objects.filter(assignment=asn).exists():
        progress += 25
      if Course.objects.filter(assignment=asn).exists():
        progress += 25
      if Criterion.objects.filter(assignment=asn).exists():
        progress += 25
    progresses.append(progress)

  # FORMS:
  # TODO: Set the correct school based on login
  assignmentForm = AssignmentForm(initial={'school': assignments[0].school})

  if request.method == 'POST':
    if 'add-assignment' in request.POST:
      assignmentForm = AssignmentForm(request.POST)
      if assignmentForm.is_valid():
        assignmentForm.save()
        return redirect('assignments')
    elif 'delete-assignment' in request.POST:
      assignmentID = request.POST.get('assignmentid', None)
      Assignment.objects.filter(id=assignmentID).delete()
      return redirect('assignments')

  context = {'assignments': assignments, 'progresses': progresses, 'assignmentForm': assignmentForm}
  return render(request, 'assignment_list.html', context)

# The wrapper function for the solver, that should be called when the button to
# solve is clicked on the website, on some inputted data and with some inputted
# constraints.
# See: https://developers.google.com/optimization/mip/integer_opt


def distribute_students(assignment, courses, students, criteria, student_course_associations):

  # creating student bounds
  student_max_bound = 3
  student_bounds = {}
  for student in students:
    student_bounds[student.id] = student_max_bound

  # creating student coeffs
  student_coeffs = {}
  for student in student_bounds:
    student_coeffs[student] = {}
  for association in student_course_associations:
    student_coeffs[association.student.id][association.course.name] = association.priority

  # creating course bounds
  course_bounds = {}
  for course in courses:
    course_bounds[course.name] = course.max_capacity

  # Create the mip solver with the SCIP backend.
  solver = pywraplp.Solver.CreateSolver('SCIP')

  # Create variable dictionary for modelling.
  variables = {}
  for student in student_bounds:
    variables[student] = {}
    for course in course_bounds:
      variables[student][course] = solver.BoolVar(course)

  # Create student course selection constraints.
  for student in student_bounds:
    constraint_student = solver.RowConstraint(student_bounds[student], student_bounds[student], '')
    for course in course_bounds:
      constraint_student.SetCoefficient(variables[student][course], 1)

  # Create course capacity constraints.
  for course in course_bounds:
    constraint_course = solver.RowConstraint(0, course_bounds[course], '')
    for student in student_bounds:
      constraint_course.SetCoefficient(variables[student][course], 1)

  # Create maximization objective function.
  objective = solver.Objective()
  for student in student_bounds:
    for course in course_bounds:
      objective.SetCoefficient(variables[student][course], student_coeffs[student][course])
  objective.SetMaximization()

  status = solver.Solve()

  # student is an id, course is a name
  for student in student_bounds:
    for course in course_bounds:
      Student_Course_Association.objects.filter(student=student, course__name=course).update( assigned = bool(variables[student][course].solution_value()) )


def assignment(request, item):
  assignment = Assignment.objects.get(pk=item)
  # In the future obtain the school from which user is logged in
  # Right now it's only used to identify the teachers, but its e-mail address
  # should also be in # the top menu
  school = assignment.school
  students = Student.objects.filter(assignment=item)
  courses = Course.objects.filter(assignment=item)
  # No direct foreign key to check on :/ :
  # Instead we check that the course matches one of the assignment courses
  student_course_associations = Student_Course_Association.objects.filter(course__in=courses)
  criteria = Criterion.objects.filter(assignment=item)

  teachers = Teacher.objects.filter(school=school)

  #if request.method == 'POST':
  #  message = request.POST['message']
  #  send_mail('Invitations Emails', 
  #            message, 
  #            settings.EMAIL_HOST_USER, 
  #            ['tariqzaman1@hotmail.com'], 
  #            fail_silently=False) 



  # FORMS
  criterionForm = CriterionForm(initial={'assignment': assignment})
  studentForm = StudentForm(initial={'assignment': assignment})
  courseForm = CourseForm(initial={'assignment': assignment})
  uploadStudentsCSVForm = UploadStudentsCSVForm(initial={'assignment': assignment})
  emailForm = EmailForm(initial={'assignment': assignment})

  # Other GET forms from this view here
  if request.method == 'POST':
    # Identify which form was submitted
    if 'add-student' in request.POST:
      studentForm = StudentForm(request.POST)
      # breakpoint()
      if studentForm.is_valid():
        studentForm.save()
    elif 'delete-student' in request.POST:
      studentID = request.POST.get('studentid', None);
      Student.objects.filter(id=studentID).delete()
    elif 'add-course' in request.POST:
      courseForm = CourseForm(request.POST)
      if courseForm.is_valid():
        courseForm.save()
    elif 'edit-course' in request.POST:
      courseName = request.POST.get('name', None);
      Course.objects.filter(name=courseName).get()
      if courseForm.is_valid():
        courseForm.save()
    elif 'delete-course' in request.POST:
      courseID = request.POST.get('courseid', None);
      Course.objects.filter(id=courseID).delete()
    elif 'import-students' in request.POST:
      form = UploadStudentsCSVForm(request.POST, request.FILES)
      # TODO: Better validation
      if form.is_valid():
        upload_students_csv_handler(assignment, request.FILES['file'])
    elif 'distribute-students' in request.POST:
      # TODO: Shouldn't need students in the future, but courses are still
      # needed as max capacity is set there.
      distribute_students(assignment, courses, students, criteria, student_course_associations)
      #return HttpResponseRedirect('{% url 'assignment' %}')
    elif 'send-inv-email' in request.POST: 
      subject = request.POST['invitation_email_subject']
      message = request.POST['invitation_email_message']
      send_mail('Invitations Email',
                subject,
                message, 
                settings.EMAIL_HOST_USER, 
                ['tariqzaman1@hotmail.com'], 
                fail_silently=False) 


  # /FORMS

  context = {'assignment': assignment, 'students': students, 'courses':
      courses, 'student_course_associations': student_course_associations,
      'teachers': teachers, 'criteria': criteria, 'studentForm': studentForm,
      'criterionForm': criterionForm, 'courseForm': courseForm,
      'uploadStudentsCSVForm': uploadStudentsCSVForm, 'emailForm': emailForm
  }

  return render(request, 'assignment.html', context)


# A generic view!: https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/
#class AssignmentListView(ListView):
#    # Obtain the school from which user is logged in
#    # school =
#
#    model = Assignment
#
#
#
#    # This is really the default name of the template it expects, but it
#    # looks at the root of the app name (main) by default, so I specify it here
#    # to make it look in all template dirs.
#    template_name="assignment_list.html"
#
#    # If we want to pass additional data to the template
#    def get_context_data(self, **kwargs):
#        # Call the base implementation first to get a context
#        context = super().get_context_data(**kwargs)
#
#
#        # CALCULATE THE PROGRESS ON THE ASSIGNMENT (PROGRESS BAR)
#
#        self.progresses = []
#        for asn in Assignment.objects.all():
#          # If results e-mail has been sent there's no need for the subsequent
#          # calculations?
#          progress = 0
#          if asn.results_email_sent:
#            progress = 100
#          else:
#            if Student.objects.filter(assignment=asn).exists():
#              progress += 25
#            if Course.objects.filter(assignment=asn).exists():
#              progress += 25
#            # This seems annoying/silly at this point, maybe a criterion should have a
#            # direct connection with assignment?
#            if Criterion.objects.filter(assignment=asn).exists():
#              progress += 25
#          self.progresses.append(progress)
#
#        context['progresses'] = self.progresses
#        return context



# Export student course assignments
# https://docs.djangoproject.com/en/3.2/howto/outputting-csv/
import csv

from django.http import StreamingHttpResponse

class Echo:
  """An object that implements just the write method of the file-like
  interface.
  """
  def write(self, value):
    """Write the value by returning it, instead of storing in a buffer."""
    return value

def download_csv(request, item):
  """A view that streams a large CSV file."""

  assignment = Assignment.objects.get(pk=item)
  students = Student.objects.filter(assignment=item)
  # No direct foreign key to check on :/ :
  # Instead we check that the course matches one of the assignment courses
  #student_course_associations = Student_Course_Association.objects.filter(student__in=students).order_by('student')
  student_course_associations = Student_Course_Association.objects.filter(student__in=students)
  rows = []
  for st in students:
    courses_assigned = []
    for sca in student_course_associations:
      if sca.student == st and sca.assigned:
        courses_assigned.append(sca.course.name)

    rows.append((st.email_address, ",".join(courses_assigned)))

  pseudo_buffer = Echo()
  writer = csv.writer(pseudo_buffer)
  return StreamingHttpResponse(
    (writer.writerow(row) for row in rows),
    content_type="text/csv",
    headers={'Content-Disposition': 'attachment; filename="courses-assigned.csv"'},
  )


def upload_students_csv_handler(assignment, file):
  breakpoint()

  reader = csv.reader(file)
  for row in reader:
    _, created = Student.objects.get_or_create(
    first_name=row[0],
    email_address=row[1],
    )
  return redirect(f'assignment/{assignment}')
