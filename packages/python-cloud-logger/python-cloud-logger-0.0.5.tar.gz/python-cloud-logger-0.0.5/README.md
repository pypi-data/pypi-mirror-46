# python-cloud-logger

A logger with thread local storage for logging context in all logs without repeating the code. This is a json logger where some contextual fields need to be included in every log per request/thread in a safe and efficient way.

Note that, all the loggers retrieved on that particular thread ( by using logging.getLogger ) will inherit the context.

## Usage
```python

from pythoncloudlogger import *

logger=logging.getLogger("myapp-logger")

logger.updateContext({
  "requestId" : "1245"
})

logger.info("Request successfully processed")

logger.clearContext()

```
