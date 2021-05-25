from django.shortcuts import render
from django.views.generic import ListView
from main.models import Assignment

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
  context = {'assignment': assignment}

  return render(request, 'assignment.html', context)
