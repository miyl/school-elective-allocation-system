#!/usr/bin/env sh

if [ -z "$1" ]; then exit; fi

if [ "$1" = 'runl' ]; then
  . env/bin/activate && school_elective_assigner/manage.py runserver
elif [ "$1" = 'runw' ]; then
  . env/Scripts/activate && python.exe school_elective_assigner/manage.py runserver
fi
