from django.shortcuts import render
from django.views.generic import ListView
from main.models import Assignment, Student, Course, Student_Course_Request, Student_Course_Assignment

def index(request):
   context = {}

   return render(request, 'index.html', context)

# A generic view!: https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/
class AssignmentListView(ListView):

    model = Assignment

    # This is really the default name of the template it expects, but it
    # looks at the root of the app name (main) by default, so I specify it here
    # to make it look in all template dirs.
    template_name="assignment_list.html"

    # If we want to pass additional data to the template
    #def get_context_data(self, **kwargs):
    #    # Call the base implementation first to get a context
    #    context = super().get_context_data(**kwargs)
    #    # Add in a QuerySet of all the books
    #    context['book_list'] = Book.objects.all()
    #    return context

#def assignments(request):
#   context = {}
#
#   return render(request, 'assignments.html', context)

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
  students = Student.objects.filter(assignment=item)
  courses = Course.objects.filter(assignment=item)
  # No direct foreign key to check on :/ :
  # Instead we check that the course matches one of the assignment courses
  student_course_requests = Student_Course_Request.objects.filter(course__in=courses)
  student_course_assignments = Student_Course_Assignment.objects.filter(course__in=courses)
  #criteria = Assignment.objects.get(pk=item)
  context = {'assignment': assignment, 'students': students, 'courses':
      courses, 'student_course_requests': student_course_requests,
      'student_course_assignments': student_course_assignments}

  return render(request, 'assignment.html', context)
