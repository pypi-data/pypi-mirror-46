# frd_logging



## Build 

```
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Upload

```
twine upload dist/*
```

## Install

```
pip install frd_logging
```

# Usage

``` python
import frd_logging
logger = frd_logging.get_loggger()
logger.debug('hello')
```
