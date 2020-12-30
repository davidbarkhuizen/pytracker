# pyTracker

single-thread python back-tracker / spider framework  
with knight's tour sample implementation

## Model

### Decider
- solution_status(self)
- get_child_states(self, parent_state)
- filter_useful_states_to_children(self, useful_states, max_children_to_use)

### BackTracker
- solve(self, decider=None, initial_state=None)

## Usage

```
$ python3 knights_tour.py --size 5
```