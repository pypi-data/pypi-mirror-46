# -*- coding unix -*-

import yaml

sampleSprint = """
    sprints:
      Sample Sprint:
        active: True
        start: "2019-04-02"
        end: "2019-04-16"
        stories:
          -
            - Story Name 1
            - This is the description
            - 10
            - big
            - to-do
            - null
          -
            - Story Name 2
            - This is another description
            - 10
            - big
            - to-do
            - "2019-04-03"
          -
            - Story Name 3
            - This is another description
            - 10
            - big
            - to-do
            - "2019-04-04"
          -
            - Story Name 4
            - This is another description
            - 10
            - big
            - to-do
            - "2019-04-05"
          -
            - Story Name 5
            - This is another description
            - 10
            - big
            - to-do
            - "2019-04-06"
"""

def initializeDocument():
    """Initialize Lmrt4uFile in current directory"""
    with open('Lmrt4uFile', 'w') as new_file:
        contents = yaml.safe_load(sampleSprint)
        yaml.dump(contents, new_file)

def main():
    initializeDocument()

if __name__ == "__main__":
    main()
