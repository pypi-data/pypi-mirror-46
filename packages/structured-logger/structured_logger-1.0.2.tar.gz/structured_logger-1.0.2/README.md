# Structured Logger

This logger has been written in an attempt to provide structured logging around Python's default `logging` library. Potential uses include adding additional objects to be parsed and filtered by in an Elastic stack.

This library may be used if structured JSON log output is desired, without the potential overkill of a full implementation such as `structlog`. This isn't to take anything away from `structlog`, and for large projects it may still be a preferable option.

## Usage

The logger should be used in a similar fashion to the Python `logging` package. Without additional context keys, it may be used as below:

```python
from structured_logger import Logger

logger = Logger(__name__)
logger.set_level("DEBUG") # This could be set by an environment variable

def test_function():
    do_a_thing()
    logger.info("this is a typical logging message")
```

However, additional context may be output by passing a `dict` of parameters following the message:

```python
from structured_logger import Logger

logger = Logger(__name__)
logger.set_level("DEBUG") # This could be set by an environment variable

def test_function():
    user_info = login()
    logger.info("user logged in", {"user": user_info})
```

Finally, the `error()` function will provide additional stack trace information by default, and exception information where appropriate:

```python
from structured_logger import Logger

logger = Logger(__name__)
logger.set_level("DEBUG") # This could be set by an environment variable

def test_function():
    try:
        something_that_raises_a_value_error()
    except ValueError:
        logger.error("a value error has been thrown")
```

The above should output JSON with additional information in the fields `errorName`, `errorMessage` and `errorStackTrace`.
