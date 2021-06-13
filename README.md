# School Elective Allocation System

KEA Datamatiker Final Project June 2021

[![GitHub Super-Linter](https://github.com/miyl/school-elective-allocation-system/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Guide

The included testing database has the following super user available:  

Username: a  
Password: a

#### Installation

```bash
1. https://github.com/miyl/school-elective-allocation-system.git # clone repo
2. cd school-elective-allocation-system                          # enter repo directory
3. python -m venv env                                            # create a virtual env
4. Now things differ on Linux and Windows:
   Linux:
   . env/bin/activate                                            # enter the virtual env
   Windows:
   . env\Scripts\activate                                        # enter the virtual env
5. pip install -r requirements.txt                               # install packages into the virtual env
```

#### Run

Linux:
```bash
1. . env/bin/activate                                            # enter the virtual env
2. ./school_elective_assigner/manage.py runserver                # start the dev-server locally
```

Windows:
```bash
1. . env/Scripts/activate                                        # enter the virtual env
2. python.exe .\school_elective_assigner\manage.py runserver     # start the dev-server locally
```

or use this **cross platform** solution:
```bash
./helper.sh run                                                  # start the dev server locally
```
