# Kryptic Studio - KrypticLogger

KrypticLogger is a tool to help better organize and minimizing the amount of code while logging!

## Installation
1. Pip Installation
```bash
pip install KrypticLogger
```
### OR

1. Clone Repository to Project Folder.
```bash
$ git clone https://github.com/KrypticStudio/KrypticLogger
```
2. Install requirements
```bash
$ pip install -r requirements.txt
```
3. Install setup.py
```bash
$ python3 setup.py install
```

## Usage
1. Import KrypticLogger!
```python
from KrypticLogger import log #as log
import KrypticLogger as logPath
```
2. Call it anywhere!
```python
#### Set path for log file
	logPath.path = "Logs/log.txt"
### Parameters
    # tag = "EXAMPLE" #Customize the notifier tag. ##ONLY AVAILABLE FOR CUSTOM
    # log = True #Logs to terminal or cmd.
    # write = False #Writes log to file
    # time = False #Adds current time to log
    # code = "0x00" #Custime code for error, organization, etc...
    # critical = False #Displays weather the message is critical or not.
log.custom(tag, message, log = True, write = False, time = False, code = "", critical = False)
```
3. EXAMPLE
```python
# Example
from KrypticLogger import log
import KrypticLogger as logPath

# Setting Log Path(Optional) ***DEFAULT "log.txt"
logPath.path = "Logs/log.txt"

#Message to be displayed...
Message = "Kryptic Studio Test. Kryptic Logger"

# Calling Logs
log.debug(Message)
log.error(Message)
log.info(Message)
log.log(Message)
log.success(Message)
log.track(Message)
log.warn(Message) 
log.custom("Custom Tag", Message)
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
