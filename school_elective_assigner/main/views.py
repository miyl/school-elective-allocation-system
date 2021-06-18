from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import (Assignment, Student, Course,
     Student_Course_Association, Teacher, Criterion)
from .forms import ( StudentForm, CriterionForm, CourseForm, AssignmentForm,
  UploadStudentsCSVForm )

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
      assignmentID = request.POST.get('assignmentid', None);
      Assignment.objects.filter(id=assignmentID).delete()
      return redirect('assignments')

  context = {'assignments': assignments, 'progresses': progresses, 'assignmentForm': assignmentForm}
  return render(request, 'assignment_list.html', context)

# The wrapper function for the solver, that should be called when the button to
# solve is clicked on the website, on some inputted data and with some inputted
# constraints.
# See: https://developers.google.com/optimization/mip/integer_opt
def distribute_students(assignment, courses, students, criteria, student_course_associations):
  print("It's working! Jar-Jar it's working!")
  #from ortools.linear_solver import pywraplp
  #solver = pywraplp.Solver.CreateSolver('SCIP')

  # ADD VALUES TO BE SOLVED
  # The values below are min and max values
  #x = solver.IntVar(0.0, 5, 'x')
  #y = solver.IntVar(0.0, 5, 'y')

  # ADD CONSTRAINTS / CRITERIA
  # x + 7 * y <= 17.5.
  #solver.Add(x + 7 * y <= 17.5)

  # DEFINE THE OBJECTIVE
  # Maximize x + 10 * y.
  #solver.Maximize(x + 10 * y)

  # RUN THE SOLVER
  #status = solver.Solve()

  # PRINT SOLUTION
  #if status == pywraplp.Solver.OPTIMAL:
  #    print('Solution:')
  #    print('Objective value =', solver.Objective().Value())
  #    print('x =', x.solution_value())
  #    print('y =', y.solution_value())
  #else:
  #    print('The problem does not have an optimal solution.')

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



  # FORMS
  criterionForm = CriterionForm(initial={'assignment': assignment})
  studentForm = StudentForm(initial={'assignment': assignment})
  courseForm = CourseForm(initial={'assignment': assignment})
  uploadStudentsCSVForm = UploadStudentsCSVForm(initial={'assignment': assignment})
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
      # TODO: Validation
      if form.is_valid():
        upload_students_csv_handler(request.FILES['file'])
    elif 'distribute-students' in request.POST:
      # TODO: Shouldn't need students in the future, but courses are still
      # needed as max capacity is set there.
      distribute_students(assignment, courses, students, criteria, student_course_associations)
      #return HttpResponseRedirect('{% url 'assignment' %}')


  # /FORMS

  context = {'assignment': assignment, 'students': students, 'courses':
      courses, 'student_course_associations': student_course_associations,
      'teachers': teachers, 'criteria': criteria, 'studentForm': studentForm,
      'criterionForm': criterionForm, 'courseForm': courseForm,
      'uploadStudentsCSVForm': uploadStudentsCSVForm
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


def upload_students_csv_handler(file):
  print("WOOOOOOHOOO")
  breakpoint()

  with open(path) as f:
    reader = csv.reader(f)
    for row in reader:
      _, created = Teacher.objects.get_or_create(
      first_name=row[0],
      last_name=row[1],
      middle_name=row[2],
      )
