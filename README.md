# Min-Max-Reversi
### Christian Martano, Justin Moczynski, Gabe Pesco, Milo Rue

## Introduction
What are the different strategies for winning a game of Reversi (or Othello)? How does the number of tiles one gains on their turn affect the game's outcome? What parts of the board have higher value? How does the order of moves affect the game's outcome? Different strategies for playing Reversi were programmed and analyzed when played against each other.

## Attempted Agents
### Agent: Mini-Max With Pruning
* **Author**: Justin Moczynski
* **Description**: Mini-Max player which prunes out unnecessary branches in the tree representing all of the possible game states by move in order to decrease the amount of time a Mini-Max player takes to play a move.
* **Benefits**: This player's turn speed will be greatly decreased as it does not check every possible board state after every possible move if the player has already found an acceptable move.
* **Drawbacks**: This player, if not programmed correctly, can be hindered in both the speed at which it makes moves and the end result of the game.
* **Conclusion**: This player was not programmed correctly: the time it took to calculate moves was slower than the original Mini-Max player and it was losing constantly to the original Greedy player.
* **What Went Wrong**:

## Final Agents
### Agent 1: Corner-Heuristic Agent with Random Optimal Choices
* **Author**: Milo Rue
* **Description**: Default Mini-Max Agent with a heuristic towards favoring corners and moves that would lead to it occupying a corner. It also avoids moves that would give the opponent the corner position. When scores pulled from min-max are the same it will randomly pick from those choices.
* **Benefits**: It is able to reliable beat default mini-max and it doesn't always repeat the same games as default did due to the random pick of optimal choices.
* **Drawback**: It has marginal improvements on default mini-max and sometimes blindly picking corners is actually bad for it and makes it lose vs. other mini-max variants we tried.
* **Conclusion**: Although this agent is an improvement on mini-max it needs to have a more robust heuristic for determining moves and still needs the improvements in depth of trees.
### Agent 2: Edge/Corner-Heuristic Agent with Ordered Choices
Description
Benefits
Drawback
Conclusion
### Agent 3: Quiescence-Based Agent
* **Author**: Christian Martano
* **Description**: MinMax agent that uses quiescence search in order to determine at what depth within the search tree is the game state stable enough to return minmax values back up the search tree. It does so by calculating a “stability value” that is based off of the total number of moves that both the min and max player have. 
* **Benefits**: Removes the hard coding of a depth threshold for the algorithm should now know where is the best to stop searching down the tree. Beats the random and greedy player agents at high rates. 
* **Benefits**: Removes the hard coding of a depth threshold for the algorithm should now know where is the best to stop searching down the tree. Beats the random and greedy player agents at high rates on smaller boards. 
* **Drawback**: Takes much longer than hardcoded depth threshold for it will continue to look down the tree until it finds stable board states. 
* **Conclusion**: While this agent works great for smaller boards, it takes a very long time in 8x8 environments for the search tree is so much larger. If there are time limits for indiviual moves, this agent will not do very well.
### Agent 4: Mini-Max Agent with Alpha/Beta Pruning
Description
Benefits
Drawback
Conclusion
