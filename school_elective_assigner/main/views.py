from django.shortcuts import render
from django.views.generic import ListView
from .models import (Assignment, Student, Course, Student_Course_Request,
     Student_Course_Assignment, Teacher, Criterion)
from .forms import StudentForm, CriterionForm, CourseForm, AssignmentForm

def index(request):
  context = {}

  return render(request, 'index.html', context)


def assignments(request):
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
      # This seems annoying/silly at this point, maybe a criterion should have a
      # direct connection with assignment?
      if Criterion.objects.filter(assignment=asn).exists():
        progress += 25
    progresses.append(progress)

  # FORMS:

  if request.method == 'POST':
    if 'add-assignment' in request.POST:
      assignmentForm = AssignmentForm(request.POST)
      if assignmentForm.is_valid():
        print("VALID")
        assignmentForm.save()
  else: # GET
    assignmentForm = AssignmentForm()

  context = {'assignments': assignments, 'progresses': progresses, 'assignmentForm': assignmentForm}
  return render(request, 'assignment_list.html', context)

# The wrapper function for the solver, that should be called when the button to
# solve is clicked on the website, on some inputted data and with some inputted
# constraints.
# See: https://developers.google.com/optimization/mip/integer_opt
def solve():
  pass
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
  student_course_requests = Student_Course_Request.objects.filter(course__in=courses)
  student_course_assignments = Student_Course_Assignment.objects.filter(course__in=courses)
  #criteria = Assignment.objects.get(pk=item)

  teachers = Teacher.objects.filter(school=school)

  # FORMS
  criterionForm = CriterionForm()
    # Other GET forms from this view here
  if request.method == 'POST':
    # Identify which form was submitted
    if 'add-student' in request.POST:
      studentForm = StudentForm(request.POST)
      # breakpoint()
      if studentForm.is_valid():
        studentForm.save()
    elif 'add-course' in request.POST: 
      courseForm = CourseForm(request.POST)
      if courseForm.is_valid():
        courseForm.save()
  else: # GET
    studentForm = StudentForm()
    courseForm = CourseForm()


  # /FORMS

  context = {'assignment': assignment, 'students': students, 'courses':
      courses, 'student_course_requests': student_course_requests,
      'student_course_assignments': student_course_assignments, 'teachers':
      teachers, 'studentForm': studentForm, 'criterionForm': criterionForm, 
      'courseForm': courseForm
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
