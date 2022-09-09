# -*- coding:utf-8 -*-
#from __future__ import print_function
import sys, os, time, re, math, collections, json
import numpy as np
import itertools
from itertools import chain
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL
import multiprocessing as mp

try:
   import pickle as pickle
except:
   import pickle


############################################
#        Logging
############################################

def logManager(logger_name='main', 
              handler=StreamHandler(),
              log_format = "[%(levelname)s] %(asctime)s - %(message)s",
              level=DEBUG):
    formatter = Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    logger = getLogger(logger_name)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def timewatch(logger=None):
  if logger is None:
    logger = logManager(logger_name='utils')
  def _timewatch(func):
    def wrapper(*args, **kwargs):
      start = time.time()
      result = func(*args, **kwargs)
      end = time.time()
      logger.info("%s: %f sec" % (func.__name__ , end - start))
      return result
    return wrapper
  return _timewatch
