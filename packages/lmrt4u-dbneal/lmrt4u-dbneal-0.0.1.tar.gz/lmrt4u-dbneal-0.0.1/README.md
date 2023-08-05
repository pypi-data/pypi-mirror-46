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

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Credits & References

Python module template taken from [mtchavez/python-package-boilerplate](https://github.com/mtchavez/python-package-boilerplate)

SDD template taken from  [CSUF Course COP3331 Template](http://www.cs.fsu.edu/~lacher/courses/COP3331/sdd.html)
