let-me-render-that-4u (lmrt4u)
==========================

Python Package for the lmrt4u agile artefact render tool

## Package

Basic structure of package is

```
├── README.md
├── lmrt4u
│   ├── __init__.py
│   ├── __main__.py
│   ├── controller.py
│   ├── entry.py
│   ├── helpers.py
│   ├── initializer.py
│   ├── interface.py
│   ├── loader.py
│   ├── parser.py
│   ├── renderer.py
│   ├── tuples.py
│   └── validator.py
├── requirements.txt
└── setup.py
```

## Installation
To install the tool without the use of  the code repository

```
pip install -i https://test.pypi.org/simple/ lmrt4u
```

## Usage

To run the tool do

```
python -m lmrt4u
```

This generates a sample Lmrt4ufile in current directory. File can be modified manually then re-run to display updated sprint information.

To run the tool without leveraging to user interface you can pass arguments directly

```
python -m lmrt4u Burndown Chart
```

### Lmrt4uFile

The Lmrt4uFile contains the backlog information that will be used when the burndown charts are generated. Please note that all sprint properties are enforced through a verification module
so make sure to follow the configuration guide below.

Here's a brief example  of the file (All information in parenthesis is for the user and should NOT be included in the file):

```
sprints: (List of sprints contained in the backlog, sample file contains one but you can include as many as you'd like)
  Sample Sprint: (This is the name of a sprint)
    active: true (A boolean property, if a sprint is active (True) then a burndown chart will be generated)
    end: '2019-04-16' (End date for the sprint, *must occur after the start date*, *must match format 'yyyy-MM-DD'*)
    start: '2019-04-02' (Start date for the sprint, *must match format 'yyyy-MM-DD'))
    stories: (List of arguments with each unique item representing a story)
    - - Story Name 1 (This is the name of a story in the sprint)
      - This is the description (This is the description for the story)
      - 10 (This is the amount of story points assigned to the story)
      - '2019-04-03' (This is the completion date, put null if the story is yet to be completed)
```

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Credits & References

Python module template taken from [mtchavez/python-package-boilerplate](https://github.com/mtchavez/python-package-boilerplate)

SDD template taken from  [CSUF Course COP3331 Template](http://www.cs.fsu.edu/~lacher/courses/COP3331/sdd.html)
