CMPT 417 - Intelligent Systems 
Fall 2022 

Mahtab Rae, mnazari
Cagla Istanbulluoglu, cistanbu
Hareet Dhillon, hareetd

Please run the connect4_CMPT417.py file if you would like to replicate the experiment results. 

For the correct usage, refer to:

usage: connect4_CMPT417.py [-h] [-ai] [-cm] [-cet] [-cw]

Play Connect 4.

options:
  -h, --help            show this help message and exit
  -ai, --ai_only        play the Minimax (with alpha-beta pruning) and Monte Carlo tree search algorithms against each other
  -cm, --compare_minimax
                        compare Minimax and Minimax with alpha-beta pruning on search tree depth vs. average execution times
  -cet, --compare_execution_times
                        compare average execution times for Minimax with alpha-beta pruning and Monte Carlo tree search
  -cw, --compare_wins   compare Minimax and Monte Carlo tree search on which one wins more across 10 runs
