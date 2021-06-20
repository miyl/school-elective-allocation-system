from random import randint, choice

num_courses = 7
num_students = 300

num = 0
for i in range(0,num_students):
  pril = [f for f in range(1, num_courses+1)]
  corl = [f for f in range(1, num_courses+1)]
  for n in range(0, num_courses):
    pri = choice(pril)
    pril.remove(pri)

    # This works so long as the course ID's start from zero...
    cor = choice(corl)
    corl.remove(cor)
    print( (
    "{"
      "\"model\": \"main.student_course_request\","
      f"\"pk\": {num},"
      "\"fields\": {"
        f"\"priority\": {pri},"
        f"\"course\": {cor},"
        f"\"student\": {i}"
      "}"
    "},"

    ) )
    num += 1
