import setuptools


setuptools.setup(name='lmrt4u-dbneal',
                 version="0.0.1",
                 author='Dillon ONeal',
                 author_email='doneal@csu.fullerton.edu',
                 description='Agile project artefact generator.',
                 long_description=open('README.md').read().strip(),
                 url='https://github.com/dbneal/lmrt4u',
                 install_requires=['pyfiglet', 'clint', 'six', 'matplotlib', 'asciiplotlib', 'cerberus', 'colorama', 'termcolor', 'numpy', 'pyinquirer'],
                 long_description_content_type='text/markdown',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ]),
