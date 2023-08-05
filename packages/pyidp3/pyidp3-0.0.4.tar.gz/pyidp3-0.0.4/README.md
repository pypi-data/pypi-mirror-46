# pyidp3
Repo for the pyidp3 library. 
This is a Python3 port of [Joost Vennekens' pyidp library](https://bitbucket.org/joostv/pyidp/)

This port still contains some hardcoding. 
This project is still WIP!

[![Documentation Status](https://readthedocs.org/projects/pyidp3/badge/?version=latest)](https://pyidp3.readthedocs.io/en/latest/?badge=latest)
    

# Documentation
## Porting
* Firstly [2to3](https://docs.python.org/3.7/library/2to3.html) was used. This creates a log of the changes made, which can be found in '2to3.log'
* Secondly the way popen works was changed. In Python3 it only accepts bytes objects, thus all input had to be encoded first, and all output then had too be decoded. This was done manually using the encode() and decode() methods.
* Added a '.' in front of the relative inputs (Python3 doesn't like these)
* Fixed a bug in the Constant method
* Fixed a (minor) bug in the Constraint method, where it didn't use self.know, but rather just appended directly. The code works perfectly fine like this , but it's changed added for consistency. 

## Added features
* Comments throughout the code to better understand it
* A Minimize-function, which replaces the mainprocedure of the IDPscript with it's own functionality (TODO: CHANGE!)
* Hardcoded a SATcheck function


# Log
16/02/2019:
* removed the hardcoding in the minimize function
* added a Term block as a subclass of Block
* changed the way Block.show works so it defaults to having no models
* added comments throughout TypedIDP
* Switched the comment system over to Sphinx and reST.
* IDP.__str__ was split into 3 methods: generateScript, minimizeScript and customScript. This allows for modelgeneration, minimization and creating custom IDP scripts.

## Actual docs
The actual docs can be found over at [ReadTheDocs](https://pyidp3.readthedocs.io/en/latest/). 
This is still very rudimentary, but it should be able to supply better perspectives on the code.
