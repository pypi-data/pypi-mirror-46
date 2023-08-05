import lmrt4u.interface as interface
import lmrt4u.controller as controller
import os
import lmrt4u.initializer as initializer

def main():
    """Entry point for lmrt4u application"""
    exists = os.path.isfile('Lmrt4uFile')
    if not exists:
        initializer.initializeDocument()
    response = interface.initialize()
    controller.process(response)

if __name__ == '__main__':
    main()
