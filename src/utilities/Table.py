import os
import pickle
import numpy as np
from collections import deque
import copy
from cube import RubiksCube
from Thistlethwaites import ThistlethwaiteSolver

class LookupTable:
    """
    A class to generate, store, and retrieve lookup tables for a Thistlethwaite solver.
    Thistlethwaite's algorithm divides the Rubik's cube solution into 4 stages (G0→G1→G2→G3→G4).
    """
    
    def __init__(self, name, table_dir="tables"):
        """
        Initialize a lookup table.
        
        Args:
            name: Name of the table
            table_dir: Directory to store the tables
        """
        self.name = name
        self.table_dir = table_dir
        self.table = {}
        
        # Create directory if it doesn't exist
        if not os.path.exists(table_dir):
            os.makedirs(table_dir)
    
    def generate_table(self, start_states, is_goal_state, get_neighbors, max_depth=20):
        """
        Generate a lookup table using breadth-first search.
        
        Args:
            start_states: List of starting states
            is_goal_state: Function that returns True if a state is a goal state
            get_neighbors: Function that returns neighbors of a state
            max_depth: Maximum search depth
        """
        queue = deque([(state, 0) for state in start_states])
        visited = set(start_states)
        
        while queue:
            state, depth = queue.popleft()
            
            # Add to table
            self.table[state] = depth
            
            # Stop if we've reached max depth
            if depth >= max_depth:
                continue
                
            # Explore neighbors
            for neighbor in get_neighbors(state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        print(f"Generated table {self.name} with {len(self.table)} entries")
    
    def save(self):
        """Save the lookup table to disk."""
        path = os.path.join(self.table_dir, f"{self.name}.pkl")
        with open(path, 'wb') as f:
            pickle.dump(self.table, f)
        print(f"Saved table to {path}")
    
    def load(self):
        """Load the lookup table from disk."""
        path = os.path.join(self.table_dir, f"{self.name}.pkl")
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.table = pickle.load(f)
            print(f"Loaded table {self.name} with {len(self.table)} entries")
            return True
        else:
            print(f"Table file {path} not found")
            return False
    
    def get_value(self, state):
        """Get the value for a state from the table."""
        return self.table.get(state, None)


# Example usage for Thistlethwaite stages
def create_edge_orientation_table(max_depth=8):
    """Create lookup table for G0→G1 (orienting edges)"""
    table = LookupTable("edge_orientation")
    solver = ThistlethwaiteSolver(None)       # start from solved cube
    start_cube = RubiksCube()                 # fresh, solved
    start_hash = solver.get_state_hash(0)     # should be "000000000000"

    queue = deque([(start_cube, 0)])
    seen = {start_hash}

    while queue:
        cube, depth = queue.popleft()
        solver.cube = cube
        h = solver.get_state_hash(0)
        # record minimal depth for this hash
        if h not in table.table:
            table.table[h] = depth

        if depth == max_depth:
            continue

        # expand by all Phase 0 moves
        for mv in solver.phase_moves[0]:
            nxt = copy.deepcopy(cube)
            nxt.move(mv)
            solver.cube = nxt
            h2 = solver.get_state_hash(0)
            if h2 not in seen:
                seen.add(h2)
                queue.append((nxt, depth+1))

    print(f"Built edge‐orientation table up to depth {max_depth}: {len(table.table)} entries")
    table.save()
    return table

def create_corner_orientation_table(max_depth=10):
    """Create lookup table for G1→G2 (orienting corners and M-slice edges)"""
    table = LookupTable("corner_orientation")
    solver = ThistlethwaiteSolver(None)       # start from solved cube
    start_cube = RubiksCube()                 # fresh, solved
    solver.cube = start_cube
    start_hash = solver.get_state_hash(1)     # should be "000...000"

    queue = deque([(start_cube, 0)])
    seen = {start_hash}

    while queue:
        cube, depth = queue.popleft()
        solver.cube = cube
        h = solver.get_state_hash(1)

        # record minimal depth for this hash
        if h not in table.table:
            table.table[h] = depth

        if depth >= max_depth:
            continue

        # expand by all Phase 1 moves
        for mv in solver.phase_moves[1]:
            nxt = copy.deepcopy(cube)
            nxt.move(mv)
            solver.cube = nxt
            h2 = solver.get_state_hash(1)
            if h2 not in seen:
                seen.add(h2)
                queue.append((nxt, depth + 1))

    print(f"Built corner‐orientation table up to depth {max_depth}: {len(table.table)} entries")
    table.save()
    return table

def create_edge_permutation_table():
    """Create lookup table for G2→G3 (permuting edges into correct orbits)"""
    table = LookupTable("edge_permutation")
    # Implementation would go here
    return table

def create_final_stage_table():
    """Create lookup table for G3→G4 (final stage)"""
    table = LookupTable("final_stage")
    # Implementation would go here
    return table

if __name__ == "__main__":
    create_edge_orientation_table(8)
    create_corner_orientation_table(10)