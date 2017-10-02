# Shakuni
A ludo playing bot, written in Python. Uses heuristics based search (expecti-minimax with single ply) and TD Learning (added to branch rishab) for weight learning.

# State Space
The state of the game is maintained by two dictionaries, with key being the colour, and value being the array storing the positions for each of the pieces.  Two positions are maintained: Local (how many squares away from the starting square) and Global (square number on the board, as defined in Board.xlsx). 

# Compile/Run instructions
No need to compile. Bot can be run by calling ludo.py. Running this from client would mean running client/client 127.0.0.1 8000 ludo.py
