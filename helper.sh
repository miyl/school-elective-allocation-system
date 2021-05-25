#!/usr/bin/env sh

# Exit if zero arguments received
[ -z "$1" ] && exit

# Detect Windows
[ -f 'env/Scripts' ] && WIN=1 && WIN_ADD="python.exe"

# Load the virtual env first
if [ ! "$WIN" ]; then . env/bin/activate
else . env/Scripts/activate
fi

if [ "$1" = 'run' ]; then
  $WIN_ADD school_elective_assigner/manage.py runserver
elif [ "$1" = 'migrate' ]; then
  $WIN_ADD school_elective_assigner/manage.py makemigrations
  $WIN_ADD school_elective_assigner/manage.py migrate
elif [ "$1" = 'dump-db' ]; then
  $WIN_ADD school_elective_assigner/manage.py dumpdata --indent 2 --exclude auth.permission --exclude admin --exclude contenttypes --exclude sessions > data_dumped.json
elif [ "$1" = 'load-db' ]; then
  $WIN_ADD school_elective_assigner/manage.py loaddata data_dumped.json
fi
