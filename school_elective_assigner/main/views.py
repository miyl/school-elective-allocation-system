from django.shortcuts import render, redirect   
from .models import (Assignment, Student, Course,
     Student_Course_Association, Teacher, Criterion)
from ortools.linear_solver import pywraplp
from .forms import (InvitationEmailForm, ResultEmailForm, ReminderEmailForm,
                    StudentForm, CriterionForm, CourseForm, AssignmentForm,
                    UploadStudentsCSVForm, TeacherForm, EditDeadlineForm)
from django.conf import settings
from django.core.mail import send_mail

# Login page
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
  assignmentCreateForm = AssignmentForm(initial={'school': assignments[0].school})

  if request.method == 'POST':
    if 'add-assignment' in request.POST:
      assignmentCreateForm = AssignmentForm(request.POST)
      if assignmentCreateForm.is_valid():
        assignmentCreateForm.save()
    elif 'edit-assignment' in request.POST:
      aid = request.POST.get('id', None)
      aname = request.POST.get('name', None)
      Assignment.objects.filter(id=aid).update(name=aname)
    elif 'delete-assignment' in request.POST:
      aid = request.POST.get('id', None)
      Assignment.objects.filter(id=aid).delete()
    return redirect('assignments')

  context = {'assignments': assignments, 'progresses': progresses,
      'assignmentCreateForm': assignmentCreateForm }
  return render(request, 'assignment_list.html', context)

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
  student_course_associations = Student_Course_Association.objects.filter(course__in=courses).order_by('student', '-priority')
  for s in students:
    s.course_associations = [sca for sca in student_course_associations if sca.student == s]

  #print(students[0].first_name); print(students[0].student_course_associations)

  criteria = Criterion.objects.filter(assignment=item)

  teachers = Teacher.objects.filter(school=school)

  # FORMS
  criterionForm = CriterionForm(initial={'assignment': assignment})
  studentAddForm = StudentForm(initial={'assignment': assignment})
  courseForm = CourseForm(initial={'assignment': assignment})
  teacherForm = TeacherForm(initial={'school': school})
  uploadStudentsCSVForm = UploadStudentsCSVForm(initial={'assignment': assignment})
  invitationEmailForm = InvitationEmailForm(initial={'assignment': assignment})
  reminderEmailForm = ReminderEmailForm(initial={'assignment': assignment})
  resultEmailForm = ResultEmailForm(initial={'assignment': assignment})
  # A different approach, dynamically creating the forms but simply appending
  # them to the existing student objects instead of creating a separate
  # studentEditForms list-object
  for s in students:
    s.editForm = StudentForm(instance=s)

  for c in courses:
    c.editForm = CourseForm(instance=c)

  assignment.editForm = EditDeadlineForm(instance=assignment)

  for t in teachers:
    t.editForm = TeacherForm(instance=t)

  # Other GET forms from this view here
  if request.method == 'POST':
    # Identify which form was submitted
    if 'add-student' in request.POST:
      studentAddForm = StudentForm(request.POST)
      # breakpoint()
      if studentAddForm.is_valid():
        studentAddForm.save()
    elif 'edit-student' in request.POST:
      sid = request.POST.get('id', None)
      sfn = request.POST.get('first_name', None)
      sea = request.POST.get('email_address', None)
      Student.objects.filter(id=sid).update(first_name=sfn,
          email_address=sea)
    elif 'delete-student' in request.POST:
      studentID = request.POST.get('id', None);
      Student.objects.filter(id=studentID).delete()
    elif 'add-course' in request.POST:
      courseForm = CourseForm(request.POST)
      if courseForm.is_valid():
        courseForm.save()
    elif 'delete-course' in request.POST:
      courseID = request.POST.get('courseid', None);
      Course.objects.filter(id=courseID).delete()
    elif 'edit-course' in request.POST:
      cid = request.POST.get('id', None)
      cn = request.POST.get('name', None)
      cd = request.POST.get('description', None)
      cmc = request.POST.get('max_capacity', None)
      # Use getlist rather than get to get a list of objects!
      cts = request.POST.getlist('teachers', None)
      Course.objects.filter(id=cid).update(name=cn, description=cd,
                                           max_capacity=cmc)
      c = Course.objects.get(id=cid)
      c.teachers.set(cts)
    elif 'add-teacher' in request.POST:
      teacherForm = TeacherForm(request.POST)
      if teacherForm.is_valid():
        teacherForm.save()
    elif 'delete-teacher' in request.POST:
      id = request.POST.get('id', None)
      Teacher.objects.filter(id=id).delete()
    elif 'edit-teacher' in request.POST: 
      tid = request.POST.get('id', None)
      tfn = request.POST.get('full_name', None)
      Teacher.objects.filter(id=tid).update(full_name=tfn)
    elif 'add-criterion' in request.POST:
      criterionAddForm = CriterionForm(request.POST)
      if criterionAddForm.is_valid():
        criterionAddForm.save()
    elif 'edit-criterion' in request.POST:
      cid = request.POST.get('id', None)
      #sfn = request.POST.get('name', None)
      #a = request.POST.get('', None)
      #a = request.POST.get('', None)
      #a = request.POST.get('', None)
      #a = request.POST.get('', None)
      Criterion.objects.filter(id=cid).update()
    elif 'delete-criterion' in request.POST:
      criterion_id = request.POST.get('id', None);
      Criterion.objects.filter(id=criterion_id).delete()
    elif 'import-students' in request.POST:
      form = UploadStudentsCSVForm(request.POST, request.FILES)
      # TODO: Better validation
      if form.is_valid():
        upload_students_csv_handler(assignment, request.FILES['file'])
    elif 'allocate-courses' in request.POST:
      # TODO: Shouldn't need students in the future, but courses are still
      # needed as max capacity is set there.
      allocate_courses(assignment, courses, students, criteria, student_course_associations)
      #return HttpResponseRedirect('{% url 'assignment' %}')
    elif 'edit-deadline' in request.POST:
      aid = request.POST.get('id', None)
      adl = request.POST.get('deadline', None)
      Assignment.objects.filter(id=aid).update(deadline=adl)
      #breakpoint()
    elif 'send-inv-email' in request.POST:
      subject = request.POST.get('invitation_email_subject')
      message = request.POST.get('invitation_email_message')
      send_mail(subject,
                message,
                settings.EMAIL_HOST_USER,
                ['SchoolEmailerExam@gmail.com'],
                fail_silently=False)
    elif 'send-reminder-email' in request.POST:
      subject = request.POST.get('reminder_email_subject')
      message = request.POST.get('reminder_email_message')
      send_mail(subject,
                message,
                settings.EMAIL_HOST_USER,
                ['SchoolEmailerExam@gmail.com'],
                fail_silently=False)
    elif 'send-res-email' in request.POST:
      subject = request.POST.get('results_email_subject')
      message = request.POST.get('results_email_message')
      send_mail(subject,
                message,
                settings.EMAIL_HOST_USER,
                ['SchoolEmailerExam@gmail.com'],
                fail_silently=False)

    # Must be a better way, ie. to get the URL directly from URLs.py dynamically
    # here, just like one can in templates
    return redirect(f'/assignment/{assignment.id}')


  # /FORMS

  context = {'assignment': assignment, 'students': students,
      'courses': courses, 'teachers': teachers, 'criteria': criteria,
      'studentAddForm': studentAddForm, 'criterionForm': criterionForm,
      'courseForm': courseForm, 'invitationEmailForm': invitationEmailForm,
      'reminderEmailForm': reminderEmailForm, 'resultEmailForm':resultEmailForm,
      'uploadStudentsCSVForm': uploadStudentsCSVForm, 'teacherForm': teacherForm
  }

  return render(request, 'assignment.html', context)

def allocate_courses(assignment, courses, students, criteria, student_course_associations):

  # Parsing criteria
  student_max_bound = 0
  # TODO: Handle all the criteria types
  for crit in criteria:
    if crit.type == 1:
      student_max_bound = crit.m
    else:
      pass

  # Creating student bounds
  student_bounds = {}
  for student in students:
    student_bounds[student.id] = student_max_bound

  # Creating student coeffs
  student_coeffs = {}
  for student in student_bounds:
    student_coeffs[student] = {}
  for association in student_course_associations:
    student_coeffs[association.student.id][association.course.name] = association.priority

  # Creating course bounds
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

  # Run the solver
  status = solver.Solve()

  # Update the database with the results
  # student is an id, course is a name
  for student in student_bounds:
    for course in course_bounds:
      Student_Course_Association.objects.filter(student=student, course__name=course).update( assigned = bool(variables[student][course].solution_value()) )

  return redirect(f'/assignment/{assignment.id}')



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
  #student_course_associations = Student_Course_Association.objects.filter(student__in=students)
  student_course_associations = Student_Course_Association.objects.filter(student__in=students).order_by('student', '-priority')
  for s in students:
    s.course_associations = [sca for sca in student_course_associations if sca.student == s]
  rows = []
  for s in students:
    courses_assigned = []
    for sca in s.course_associations:
      if sca.assigned:
        courses_assigned.append(sca.course.name)

    rows.append((s.email_address, ",".join(courses_assigned)))

  pseudo_buffer = Echo()
  writer = csv.writer(pseudo_buffer)
  return StreamingHttpResponse(
    (writer.writerow(row) for row in rows),
    content_type="text/csv",
    headers={'Content-Disposition': 'attachment; filename="courses-assigned.csv"'},
  )


# Consider updating this to also support importing an identifier for the
# student (e.g. e-mail address) and a list of priorities!
def upload_students_csv_handler(assignment, file):

  reader = csv.reader( file.read().decode('utf-8').splitlines() )


  type = None
  for row in reader:
    if not type: # Why inside the loop? Because it's a generator, I think, so I
      # can't just index into the reader to check the row as that results in
      # this error:
      # '_csv.reader' object is not subscriptable

      # Determine the format super crudely:
      if "@" in row[0]:
        type = 0 # Assuming: e-mail-address + list of priorities
      else:
        type = 1 # Assuming: name + e-mail address

    # unpacking list + tuple
    email_address = row[0]
    if type == 0:
      _, created = Student.objects.get_or_create(
          assignment = assignment,
          # Set the name to the e-mail address as well...
          email_address = row[1],
          first_name = email_address,
      )
      # Priorities: Assume the rest of the row are priorities
      priorities = row[1:]
      # Loop through them two at a time, assuming the uneven ones are courses
      # and even ones priorities
      for i in range( 0, len(priorities), 2 ):
        #breakpoint()
        # If there's whitespace first between the commas this lookup would
        # fail, so stripping that first
        # course and student need IDs, so looking those up unfortunately
        # assuming names are unique
        cid = Course.objects.get(name=priorities[i].strip())
        sid = Student.objects.get(email_address=email_address.strip())
        _, created = Student_Course_Association.objects.get_or_create(
          course = cid,
          student = sid,
          priority = priorities[i+1]
        )
    else: # type 1
      _, created = Student.objects.get_or_create(
        assignment = assignment,
        first_name = row[0],
        email_address = row[1],
      )

  return redirect(f'assignment/{assignment.id}')
