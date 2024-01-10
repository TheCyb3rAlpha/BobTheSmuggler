import logging
import os

# Create a logs directory if it doesn't exist
logDir = "logs"
if not os.path.exists(logDir):
    os.makedirs(logDir)

# Define log file paths
ErrorPath = os.path.join(logDir, "errors.log")
DebugPath = os.path.join(logDir, "debug.log")

# Set up the logging format
log_format = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s] [%(process)d] [%(thread)d] - %(message)s"

def LogHandler(log_path, log_level):
    fileHandler = logging.FileHandler(log_path)
    fileHandler.setLevel(log_level)
    fileHandler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(fileHandler)

def SetLogging(verbose):
    # Configure the logging level based on the verbosity
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Add file handlers for debug and error logs
    LogHandler(DebugPath, logging.DEBUG)
    LogHandler(ErrorPath, logging.ERROR)
