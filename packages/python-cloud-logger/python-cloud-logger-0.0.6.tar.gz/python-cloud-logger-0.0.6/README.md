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

## RedactJsonFormatter

This formatter is an extension of pythonjsonlogger ( https://pypi.org/project/pythonjsonlogger ). This extension will allow you to mask fields in the json before it logs. The redaction keys are case insensitive.

### Usage
```python

# Set the environment variables
#
import logging,os

os.environ["redactionKeys"]="x-api-key,Authorization"
os.environ["redactionString"]="<secret>"

logger = logging.getLogger(__name__)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = pythoncloudlogger.RedactJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info({
	"message" : "My request details",
	"headers" : {
		# will be masked
		"x-api-key" : "sdfsf",
		"another-level" :{
			# will be masked
			"Authorization" : "Bearer dfsfd"
		}
	}

})

```