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

def assignment(request, item):
  assignment = Assignment.objects.get(pk=item)
  students = Student.objects.filter(assignment=item)
  courses = Course.objects.filter(assignment=item)
  # No direct foreign key to check on :/ :
  #student_course_requests = Student_Course_Request.objects.filter(pk=item)
  #student_course_assignments = Student_Course_Assignment.objects.filter(pk=item)
  #criteria = Assignment.objects.get(pk=item)
  #context = {'assignment': assignment}
  context = {'assignment': assignment, 'students': students, 'courses': courses}

  return render(request, 'assignment.html', context)
