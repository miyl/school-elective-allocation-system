from django.shortcuts import render

def index(request):
   context = {}

   return render(request, 'index.html', context)

def assignments(request):
   context = {}

   return render(request, 'assignments.html', context)

def assignment(request):
   context = {}

   return render(request, 'assignment.html', context)
