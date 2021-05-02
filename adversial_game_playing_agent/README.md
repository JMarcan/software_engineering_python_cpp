# Build an Adversarial Game Playing Agent

## Motivation
AI is an important topic for robotics and self-driving cars.
I did this project as part of Udacity, Artificial Intelligence Nanodegree.

## Project description
The goal of the project was to implement AI Player for the game of isolation in `my_custom_player.py`, method `get_action()`:  
I have based my AI player on **minimax search, optimized with alpha-beta pruning, enhanced with heuristics**.

![Example game of isolation on a square board](assets/game_isolation.gif)

## Isolation Game rules
In the game Isolation, two players each control their single token and alternate taking turns moving the token from one cell to another on a rectangular grid. Whenever a token occupies a cell, that cell becomes blocked for the remainder of the game. An open cell available for a token to move into is called a "liberty". The first player with no remaining liberties for their token loses the game, and their opponent is declared the winner.

In knights Isolation, tokens can move to any open cell that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. On a blank board, this means that tokens have at most eight liberties surrounding their current location. Token movement is blocked at the edges of the board (the board does not wrap around the edges), however, tokens can "jump" blocked or occupied spaces (just like a knight in chess).

Finally, agents have a fixed time limit (150 milliseconds by default) to search for the best move and respond. The search will be automatically cut off after the time limit expires, and the active agent will forfeit the game if it has not chosen a move. 

## Implemented heuristics description:
- The intuition that it’s most likely to win by prioritizing moves after which the player has more remaining possible movements than the opponent. `#my_moves – #opponent_moves`
- Defensive to offensive strategy. The weight for minimizing opp_liberties continuously increases as the game progress: `#my_moves – #(1+visited_fields_rate) *opponent_moves`
- Keeping itself closer to the center rather than to the borders. The idea is that the player has more options closer to the center, rather than closer to the borders where he can be more easily corned.  Defensive to offensive strategy applies and this feature is more prioritized at the beginning of the game and its weight continuously decreases as the game progress.

Heuristic code:
```
= ((weight / 2)*unvisited_fields_rate + len(own_liberties)) - (1+visited_fields_rate)*len(opp_liberties)
```
## Usage
1. Run `run_match.py` to test the algorithm against different AI player
    - `python run_match.py -f -r 10 -o GREEDY -p 4`
    - `-f` means fair match. If you have 10 rounds, then your player will start 10 times and the opponent player will start 10 times (in total 2x - 20 games)
    - `-r` parameter sets the number of rounds that will be played between our AI player and computer
    - `-o` parameter sets the AI opponent against which will the algorithm play. Available are: RANDOM (opponent choses random moves), GREEDY (opponent is based on greedy search), MINIMAX (opponent is based on minimax algorithm), SELF (our AI player will play against itself) 

2. You can experiment with an existing AI algorithm in `my_customer_player.py `

## Libraries used
Python 3

## Files in the repository
- `run_match.py`: contains code to execute game between your AI player and computer
- `my_algorithm.py`: contains implemented algorithm
- `sample_players.py`: contains algorithms for computer players: RANDOM (opponent choses random moves), GREEDY (opponent is based on greedy search), MINIMAX (opponent is based on minimax algorithm)