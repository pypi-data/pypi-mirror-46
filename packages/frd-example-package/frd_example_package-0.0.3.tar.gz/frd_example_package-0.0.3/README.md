# frd_example_package


## Requirements

- twine
- wheel

## Build 

```
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Upload

```
twine upload dist/*
```

# Usage

``` python
pip install frd_example_package
import frd_example_package
frd_example_package.name # >  hello world
```
