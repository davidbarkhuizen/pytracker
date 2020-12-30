# log file - run info
# solutions file - solutions and paths

import logging
from datetime import datetime

from node import Node
from state import State

class BackTracker(object):

  def __init__(self):
    n = 60
    logging.info('\n'*3)
    logging.info('-'*n)
    logging.info('pytracker - Python Back Tracker Depth First Search Spider')
    logging.info('(C) 2011 David Barkhuizen - david.barkhuizen@gmail.com')
    logging.info('-'*n)
    pass

  def solve(self, decider=None, initial_state=None):
   
    solved_count = 0
    best_solved_count = 0
    
    max_child_count = 64
    
    # init root/zero node
    current_node = Node(id=Node.next_id(), parent_id=None, state=initial_state.clone(), recursion_depth=0, decider=decider, max_child_count=max_child_count)
    current_node.upsert()
    logging.info(datetime.now())
    logging.info('root node {%i} instantiated.' % current_node.id)
    logging.info('with initial state = ')
    logging.info(str(initial_state))
    
    target_depth = initial_state.target_depth()
    # log initial state

    logging.info('creating child states...')
    current_node.create_children()
    logging.info('%i created.' % current_node.child_count)
    
    decision_path = []
    
    exit_criteria = {
      'timed_out' : False,
      'request_cancel' : False,
      'is_solved' : False,
      'solution_space_exhausted' : False,
      }
      
    rotator_counter = 0
    rotator_interval = 10000
    
    exhaust_solution_space = True

    solution_count = 0
    
    skip_solution = False
    while (True not in exit_criteria.values()):
    
      # INDICATE PROGRESS
      rotator_counter = rotator_counter + 1
      if (rotator_counter % rotator_interval == 0):
        print('node %i - current {%i}/{%i} vs. best {%i}/{%i}' % (current_node.id, solved_count, target_depth, best_solved_count, target_depth))
      
      # SOLVED
      if (decider.solution_status(current_node.state) == True) and (skip_solution == False):
        
        solution_count += 1
        
        exit_criteria['is_solved'] = True
        current_node.is_solution = True
        Node.tree[current_node.id] = current_node
        
        logging.info('node {%i} solves.' % current_node.id)
        logging.info('state:')
        logging.info(str(current_node.state))        
        
        s = 'solved: ' + str(solution_count)
        print(s)
        print(str(current_node.state))
        
        if (exhaust_solution_space == True):
          exit_criteria['is_solved'] = False
          skip_solution = True
      
      # CONTINUE
      else:
        skip_solution = False
        logging.info('solution not yet reached.')
        
        # NEED TO GENERATE CHILDREN FOR NODE
        if (current_node.next_child_idx == None):
          logging.info('need to generate children for node {%i} ...' % current_node.id)
          current_node.create_children()
          logging.info('done.  %i children created.' % current_node.child_count)
        
        # IF THE CURRENT NODE HAS AN UNEVALUATED CHILD, THEN MOVE TO IT
        if (current_node.next_child_idx != -1):
          logging.info('current node {%i} has an unevaluated child' % current_node.id)
          
          # get next child
          next_node_id = current_node.child_ids[current_node.next_child_idx]
          next_node = current_node.get(next_node_id)
          logging.info('moved fwd to unevaluated child node {%i} of parent node {%i} [child no. %i of %i]' % (next_node.id, current_node.id, current_node.next_child_idx + 1, current_node.child_count))

          # increment next child idx
          if (current_node.next_child_idx < current_node.child_count - 1):
            current_node.next_child_idx = current_node.next_child_idx + 1
          # ALL CHILDREN EXHAUSTED
          else:
            current_node.next_child_idx = -1 
          
          current_node.upsert()
          
          # NOTE MOVE FWD
          solved_count = solved_count + 1
          if (solved_count > best_solved_count):
            best_solved_count = solved_count
          logging.info("current completeness = {%i}/{%i}" % (solved_count, target_depth))
          logging.info("vs. best completeness = {%i}/{%i}" % (best_solved_count, target_depth))

          change_loc = current_node.state.locate_fwd_change(next_node.state)
          logging.info('change loc %s' % str(change_loc))

          decision_path.append(change_loc)
          logging.info('updated decision path')
          logging.info(decision_path)
          
          logging.info('new state')
          logging.info(next_node.state)
          
          # update completeness
          # current_completeness = solved_count / target_count * 100)
          # best_completeness = best_solved_count / target_count * 100)

          # increment pointer to next unevaluated remaining child (dec ## of remaining uneval children)          

          current_node = next_node

        # current_node.has_available_children() == False
        else:       
          logging.info("no unevaluated children, i.e. dead-end reached.")

          # move backwards
          # if current node has a parent, and thus it is actually possible to move backwards
          if (current_node.parent_id != None):

            # retrieve parent node
            next_node = Node.tree[current_node.parent_id]
            logging.info('moving back to parent node {%i}' % next_node.id)
            
            # locate change
            change_loc = current_node.state.locate_bwd_change(next_node.state)

            solved_count = solved_count - 1
            decision_path.pop()
            
            logging.info("current completeness = {%i}/{%i}" % (solved_count, target_depth))
            logging.info("vs. best completeness = {%i}/{%i}" % (best_solved_count, target_depth))
            
            current_node = next_node

          ## CanMoveBackwards() == False
          else:             
            exit_criteria['solution_space_exhausted'] = True
            
            logging.info('node {i%} has no parent.' % current_node.id)
            logging.info('solution space exhausted.')
       
    for exit_criterion in exit_criteria.keys():
      logging.info('%s - %s' % (exit_criterion, exit_criteria[exit_criterion]))  
    
    return exit_criteria