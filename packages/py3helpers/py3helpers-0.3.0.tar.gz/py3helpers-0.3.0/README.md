[![Build Status](https://travis-ci.org/adbailey4/python_utils.svg?branch=master)](https://travis-ci.org/adbailey4/python_utils)

# python_utils
General python functions and classes which could be used across multiple projects.

## Installation
`pip install py3helpers`  
Note: The default project does not install pysam, biopython and mappy because they are fairly large dependencies. However, if you want to use the seq_tools module you need to install via 
`pip install py3helpers[seq_tools]`  
```
git clone https://github.com/adbailey4/python_utils 
cd python_utils  
python setup.py install
pytest
```
