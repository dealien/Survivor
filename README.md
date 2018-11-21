# Survivor

A top-down open-world survival game written in Python.  

Mapgen is based on [Platypus](https://github.com/ajstensland/platypus), a Python library for terrain generation. 

Dependencies are managed using [`pip-tools`](https://pypi.org/project/pip-tools/). To automatically install all dependencies, simply use `pip-sync`. To update the dependencies, run `pip-compile --output-file requirements.txt requirements.in`. 