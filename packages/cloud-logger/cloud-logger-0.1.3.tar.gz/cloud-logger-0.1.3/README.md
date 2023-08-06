# cloud_logger

A logging library which put events to AWS Cloud Watch Logs.

## Install

```
pip install cloud_logger
```

## Setup

Set your aws access key and secret key to environment variables as follows.

```
export CLOUD_LOGGER_ACCESS_KEY_ID="XXX"
export CLOUD_LOGGER_SECRET_ACCESS_KEY="XXX"
```

## Example

```python

from __init__ import CloudLogger,CloudLoggerObject,CloudHandler
import logging

if __name__ == '__main__':
    # Setup
    logger_obj = CloudLoggerObject(
        name='LOG_GROUP_NAME',
        format='%(asctime)s : %(levelname)s : %(filename)s  a %(funcName)s %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(CloudHandler(
        logger_obj=logger_obj
    ))
    logger.setLevel(logging.DEBUG)

    # Call log
    def foobar():
        logger.error('foobar2')
        logger.warning('a')
        logger.fatal('a')

    foobar()
```

