# School Elective Allocation System

KEA Datamatiker Final Project June 2021

[![GitHub Super-Linter](https://github.com/miyl/school-elective-allocation-system/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Guide

The included testing database has the following super user available:  
Username: a  
Password: a

### Windows 

#### Installation

```bash
1. git clone url                   # cloner repo
2. cd school-elective-allocation-system # tilgå repo
3. python -m venv env              # opretter et virtual env
4. . env/Scripts/activate          # enter virtual env
5. pip install -r requirements.txt # installer pakker i virtual env
```

#### Run

```bash
1. . env/Scripts/actvate
2. python.exe .\school_elective_assigner\manage.py runserver # Starter dev-server lokalt
```
or
```bash
./helper.sh run	# Starter dev-server lokalt
```
