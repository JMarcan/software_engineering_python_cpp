import random
import time

from isolation.isolation import _WIDTH, _HEIGHT
from sample_players import DataPlayer

_CORNERS = [0, 10, 104, 114]
_WALLS = list(range(1, 10)) + list(range(105, 114)) + [i * (_WIDTH + 2) for i in range(1, _HEIGHT - 1)] + [i * (_WIDTH + 2) + (_WIDTH - 1) for i in range(1, _HEIGHT - 1)]
_CENTER = 57

from functools import reduce

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        

        if state.ply_count == 0:
            # if we do the first move, select the center
            self.queue.put(_CENTER)
        elif state.ply_count == 1:
            # if we do the second move, select wide opening
            opens = [i for i in state.actions() if i not in _CORNERS and i not in _WALLS and i != 57]
            self.queue.put(random.choice(opens))
            
        else:
            # for each other move, select the optimal minimax move at a fixed search depth of 3 plies
                 
            # Debug print final board status
            '''
            from isolation import DebugState
            dbstate = DebugState.from_state(state)
            print(dbstate)
            '''
            
            self.queue.put(self.alpha_beta_search(state, depth=3)) 
    
    def alpha_beta_search(self, state, depth):

        def min_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.heuristics(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), alpha, beta, depth-1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.heuristics(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), alpha, beta, depth-1))
                if value >= beta:
                    alpha = max(alpha, value)
            return value

        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for action in state.actions():
            v = min_value(state.result(action), alpha, beta, depth-1)
            alpha = max(alpha, v)
            if v >= best_score:
                best_score = v
                best_move = action
        return best_move


    
    def minimax(self, state, depth):
        #minimax taken from sample_players.py code

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))
    
    def heuristics(self, state):
        ''' Function to call a selected mutiple heuristiscs'''
        
        # call baseline heuristics
        # return self.score(state)
        
        #call advanced heuristics
        return self.advanced_heuristics(state)
        
    #baseline heuristics
    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
    
    def advanced_heuristics(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        
        own_distance_from_center = self.distance_from_center(own_loc)
        opp_distance_from_center = self.distance_from_center(opp_loc)
        own_distance_to_borders = self.distance_to_borders(own_loc)
        opp_distance_to_borders = self.distance_to_borders(opp_loc)
        
        unvisited_fields_rate = 1 - state.ply_count / (_HEIGHT * _WIDTH)
        visited_fields_rate = 1 - unvisited_fields_rate
        
        # if the loc close to center and away from borders, maximize move
        weight = (opp_distance_from_center - own_distance_from_center) + (own_distance_to_borders - opp_distance_to_borders)
        if weight > 0:
            # advanced heuristics based on distance from the center
            # return weight * len(own_liberties) - unvisited_fiels_rate * len(opp_liberties)
            return ((weight / 2)*unvisited_fields_rate + len(own_liberties)) - (1+visited_fields_rate)*len(opp_liberties)
        else:
            #standard heuristics based only on liberties
            return len(own_liberties) - (1+visited_fields_rate)*len(opp_liberties)
        
    def distance_from_center(self, loc):
        # Use Mahattan Distance
        center = self.xy_index_loc(57)
        player = self.xy_index_loc(loc)
        return abs(center[0] - player[0]) + abs(center[1] - player[1])

    def distance_to_borders(self, loc):
        # Get the distance to the closest border
        player = self.xy_index_loc(loc)
        return min(player[0], player[1], _WIDTH - 1 - player[0], _HEIGHT - 1 - player[1])

    def xy_index_loc(self, loc):
        return (loc % (_WIDTH + 2), loc // (_WIDTH + 2))