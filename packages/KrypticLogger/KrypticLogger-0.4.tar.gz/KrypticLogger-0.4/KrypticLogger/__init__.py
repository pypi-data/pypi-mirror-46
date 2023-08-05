#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Kryptic Studio ###

# Local Libraries

# Libraries

# Standard Libraries
import time
from sty import fg, bg, ef, rs
# Global Variables
infoText = fg.cyan + "[INFO] " + fg.rs
errorText = fg.red + "[ERROR] " + fg.rs
successText = fg.green + "[SUCCESS] " + fg.rs
warnText = fg.yellow + "[WARNING] " + fg.rs
logText = fg.white + "[LOG] " + fg.rs
debugText = fg.blue + "[DEBUG] " + fg.rs
trackText = fg.black + "[TRACK] " + fg.rs
# Function Definitions

def timeLocal():
        localtime = time.asctime(time.localtime(time.time()) )
        return(localtime)
        
path = "log.txt"

class log(object):

    @staticmethod
    def info(message, log = True, write = False, time = False):
        global infoText
        logData = infoText + message 
        logDataW = "[INFO] " + message 
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def error(message, log = True, write = False, time = False, code = "", critical = False):
        global errorText
        logData = errorText + message
        logDataW = "[ERROR] " + message
        if code != "":
            logData = fg.red + "[ERROR] " + fg.rs + message + "\n\tError: " + code
            logDataW = "[ERROR] " + message + "\n\tError: " + code
        if critical == True:
            logData += fg.red + "\tCRITICAL" + fg.rs
            logDataW += "\tCRITICAL"
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def success(message, log = True, write = False, time = False):
        global successText
        logData = successText + message
        logDataW = "[SUCCESS] " + message
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def warn(message, log = True, write = False, time = False):
        global warnText

        logData = warnText + message
        logDataW = "[WARNING] " + message
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def log(message, log = True, write = False, time = False):
        global logText
        logData = logText + message
        logDataW = "[LOG] " + message
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def debug(message, log = True, write = False, time = False):
        global debugText
        logData = debugText + message
        logDataW = "[DEBUG] " + message
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def track(message, log = True, write = False, time = False):
        global trackText
        logData =  trackText + message
        logDataW = "[TRACK] " + message
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

    @staticmethod
    def custom(tag, message, log = True, write = False, time = False, code = "", critical = False):
        global errorText
        logData = "[" + tag + "] " + message
        logDataW = "[" + tag + "] "+ message
        if code != "":
            logData = fg.red + "[ERROR] " + fg.rs + message + "\n\tCode: " + code
            logDataW = "[ERROR] " + message + "\n\Code: " + code
        if critical == True:
            logData += fg.red + "\tCRITICAL" + fg.rs
            logDataW += "\tCRITICAL"
        if time == True:
            time = "[" + timeLocal() + "] "
            logData =  time + logData
            logDataW = time + logDataW
        if log == True:
                print(logData)
        if write == True:
            logFile = open(path, "a")
            logFile.write(logDataW + "\n")
            logFile.close()

# Main Function Definition

# Main Function Definition
#def main(): ### Uncomment if nessesary!
#    return ### Uncomment if nessesary!
# Call to main()
#main() ### Uncomment if nessesary!

#or

#if __name__ == '__main__': ### Uncomment if nessesary!
#    main() ### Uncomment if nessesary!
''' 
EXAMPLE TESTING PURPOSES.
Message = "Kryptic Studio Test. Kryptic Logger"
log.debug(Message)
log.error(Message)
log.info(Message)
log.log(Message)
log.success(Message)
log.track(Message)
log.warn(Message) 
log.custom("Custom Tag", Message)
'''
