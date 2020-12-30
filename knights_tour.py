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

# 5	1,728
# 6	6,637,920
# 7	165,575,218,320
# 8	19,591,828,170,979,904

def main():
  
  n = 5 # 

  seed = datetime.now().microsecond
  random.seed(seed)
  logging.info('random seed = %i' % seed)
  
  state = State(n)
  decider = Decider()
  tracker = BackTracker()
  tracker.solve(decider=decider, initial_state=state)

if __name__ == '__main__':
  main()