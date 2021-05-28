from django import template

# Necessary prerequsite to be a valid tag filter library
register = template.Library()

# Aber why?: For looping over two lists simultaneously:
# Right now specifically a list of assignments and a list of progresses for
# each of them
@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)
