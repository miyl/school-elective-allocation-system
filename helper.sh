#!/usr/bin/env sh

if [ -z "$1" ]; then 
  exit
else
  # Load the virtual env first
  . env/bin/activate

  if [ "$1" = 'runl' ]; then
    school_elective_assigner/manage.py runserver
  elif [ "$1" = 'runw' ]; then
    python.exe school_elective_assigner/manage.py runserver
  elif [ "$1" = 'migrate' ]; then
    school_elective_assigner/manage.py makemigrations
    school_elective_assigner/manage.py migrate
  fi
fi
