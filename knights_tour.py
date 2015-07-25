from datetime import datetime
import logging
LOG_FILE_PATH = ''
LOG_FILENAME = 'knights_tour'
LOG_FORMAT = "%(message)s"

def init_logging():
  t = datetime.now()
  tstamp = ''#'%d-%d-%d-%d-%d' % (t.year, t.month, t.day, t.hour, t.minute)
  fname = LOG_FILE_PATH + LOG_FILENAME + tstamp + '.log'    
  logging.basicConfig(filename=fname, level=logging.INFO, format=LOG_FORMAT)  

init_logging()
  
# -----------------------------------------------------------------------------------------------------  

from state import State
from node import Node
from decider import Decider
from back_tracker import BackTracker
import random

def main():
  
  n = 6

  seed = datetime.now().microsecond
  random.seed(seed)
  logging.info('random seed = %i' % seed)
  
  state = State(n)
  decider = Decider()
  tracker = BackTracker()
  tracker.solve(decider=decider, initial_state=state)

if __name__ == '__main__':
  main()