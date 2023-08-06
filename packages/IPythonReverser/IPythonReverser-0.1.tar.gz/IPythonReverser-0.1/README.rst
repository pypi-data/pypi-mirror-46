About
-----

IPython reverser is a magic function for IPython that takes an argument
and returns a reversed string as the output. The sole purpose of this 
package is to show how to publish an IPython extension on PyPI.

Installation
------------

IPython reverser can be installed as a standard Python package: either from
PyPI:

::

    pip install IPythonReverser

or from git:

::

    git clone http://github.com/switowski/ipython-reverser.git 
    cd ipython-reverser/
    python setup.py install

This can be imported into an IPython shell session using either:
``import ipython_reverser`` or ``%load_ext ipython_reverser``

Although you probably want it to load when IPython loads, in which case,
edit your IPython profile file (by default
``~/.ipython/profile_default/ipython_config.py``) and add
``ipython_reverser`` to :

::

    c.TerminalIPythonApp.extensions = [
        'ipython_reverser'
    ]

(you may need to create this, and can do so with
``ipython profile create``).

Usage
-----

Just pass a string and watch how it magically gets reversed:
This can be used as a magic for a single line (line magic):

::

    In [1]: %reverse Hello world
    Out[1]: 'dlrow olleH'


