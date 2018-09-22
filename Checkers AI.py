#Checkers AI
#Isaiah Frey
#This program will play a human in a game of checkers utilizing the miniMax function and alpha beta pruning.

#Notes
#chr(9608) #Black 'Off' square
#chr(9642) #Black man
#chr(9643) #White man
#chr(9688) #White king
#chr(9689) #Black king
#chr(9824) #Spades


#------------------------Libraries--------------------------#

from random import randint
import copy


###
move_count = 0
#------------------------Classes----------------------------#
class Piece():
    
    def __init__(self, white_team, location, king=False, can_jump = False, visible = True):
        '''
        The Piece object handles all pieces on the board.
        white_team -- True if team is white
        location -- tuple (row,col)
        king -- True if the piece is a king
        can_jump -- True if the piece can make a legal jump
        visibe -- True if the piece is visible, toggle upon capture
        '''
        self.white_team = white_team
        self.king = king
        self.location = location
        self.can_jump = can_jump
        self.visible = visible
    
    #Set the string that will be printed on the board
    def __str__(self):
        if self.visible:
            #White man
            if self.white_team and not self.king:
                return chr(9643)
            #White king
            elif self.white_team and self.king:
                return chr(9688)
            #Black man
            elif not self.white_team and not self.king:
                return chr(9642)
            #Black king
            else:
                return chr(9689)
        else:
            return chr(9608)
    
    #Set the legal moves depending on the board and piece locations
    def find_legal_moves(self,board):
        
        #Initialize a list for the legal move tuples
        legal_moves = []
        
        #If the piece is off the board, return it has no legal moves
        if not self.visible:
            self.can_jump = False
            return legal_moves
        
        #Set can_jump to false until proven otherwise
        self.can_jump = False
        
        #Change the direction of checks depending on the team of the piece
        if self.white_team:
            dir = 1
        else:
            dir = -1
        
        #Check jumping possibilities first
            
        #Check towards the enemy and to the right
        #If an enemy piece is there check the square behind it
        try:
            if board[self.location[0]+dir][self.location[1]+dir].white_team != self.white_team:
                if board[self.location[0]+dir*2][self.location[1]+dir*2] == ' ':
                    #Check that the board hasn't reverse indexed
                    if self.location[0]+dir*2 >= 0 and self.location[1]+dir*2 >= 0:
                        legal_moves.append(((self.location[0]+dir*2),(self.location[1]+dir*2)))
                        self.can_jump = True
        except IndexError:
            pass
        except AttributeError:
            pass
        
        #Then check towards the enemy and to the left
        #If an enemy piece is there check the square behind it
        try:
            if board[self.location[0]+dir][self.location[1]-dir].white_team != self.white_team:
                if board[self.location[0]+dir*2][self.location[1]-dir*2] == ' ':
                    #Check that the board hasn't reverse indexed
                    if self.location[0]+dir*2 >= 0 and self.location[1]-dir*2 >= 0:
                        legal_moves.append(((self.location[0]+dir*2),(self.location[1]-dir*2)))
                        self.can_jump = True
        except IndexError:
            pass
        except AttributeError:
            pass
        
        #If the piece is a king also check the backwards directions
        if self.king:
            
            #Check towards the piece's side and to the right
            #If an enemy piece is there check the square behind it
            try:
                if board[self.location[0]-dir][self.location[1]+dir].white_team != self.white_team:
                    if board[self.location[0]-dir*2][self.location[1]+dir*2] == ' ':
                        #Check that the board hasn't reverse indexed
                        if self.location[0]-dir*2 >= 0 and self.location[1]+dir*2 >= 0:
                            legal_moves.append(((self.location[0]-dir*2),(self.location[1]+dir*2)))
                            self.can_jump = True
            except IndexError:
                pass
            except AttributeError:
                pass
            
            #Then check towards the piece's side and to the left
            #If an enemy piece is there check the square behind it
            try:
                if board[self.location[0]-dir][self.location[1]-dir].white_team != self.white_team:
                    if board[self.location[0]-dir*2][self.location[1]-dir*2] == ' ':
                        #Check that the board hasn't reverse indexed
                        if self.location[0]-dir*2 >= 0 and self.location[1]-dir*2 >= 0:
                            legal_moves.append(((self.location[0]-dir*2),(self.location[1]-dir*2)))
                            self.can_jump = True
            except IndexError:
                pass
            except AttributeError:
                pass
            
        #If the piece cannot jump then check to see where it can legally move
        if not self.can_jump:
            
            #Check towards the enemy and to the right
            #If it's open add it to the list of legal moves for that piece
            try:
                if board[self.location[0]+dir][self.location[1]+dir] == ' ':
                    #Check that the board hasn't reverse indexed
                    if self.location[0]+dir >= 0 and self.location[1]+dir >= 0:
                        legal_moves.append(((self.location[0]+dir),(self.location[1]+dir)))
            except IndexError:
                pass
            
            #Then check towards the enemy and to the left
            try:
                if board[self.location[0]+dir][self.location[1]-dir] == ' ':
                    #Check that the board hasn't reverse indexed
                    if self.location[0]+dir >= 0 and self.location[1]-dir >= 0:
                        legal_moves.append(((self.location[0]+dir),(self.location[1]-dir)))
            except IndexError:
                pass
            
            #If the piece is a king also check the backwards directions
            if self.king:
                
                #Check towards the piece's side and to the right
                #If it's open add it to the list of legal moves for that piece
                try:
                    if board[self.location[0]-dir][self.location[1]+dir] == ' ':
                        #Check that the board hasn't reverse indexed
                        if self.location[0]-dir >= 0 and self.location[1]+dir >= 0:
                            legal_moves.append(((self.location[0]-dir),(self.location[1]+dir)))
                except IndexError:
                    pass
                
                #Then check towards the piece's side and to the left
                try:
                    if board[self.location[0]-dir][self.location[1]-dir] == ' ':
                        #Check that the board hasn't reverse indexed
                        if self.location[0]-dir >= 0 and self.location[1]-dir >= 0:
                            legal_moves.append(((self.location[0]-dir),(self.location[1]-dir)))
                except IndexError:
                    pass
        
        #Return the legal moves for that piece
        return legal_moves
        
#---------------------------Initializations--------------------------#

#Decide if the player is going first
player_turn = True

#Decide if the player will play as the white pieces
player_is_white = True

#Set up the computer's team for scoring purposes
computer_is_white = False

#Set the game to not be over
game_over = False

#Dicitonary for starting piece locations
starting_loc_dict = {1:(0,1),2:(0,3),3:(0,5),4:(0,7),
                     5:(1,0),6:(1,2),7:(1,4),8:(1,6),
                     9:(2,1),10:(2,3),11:(2,5),12:(2,7),
                     13:(5,0),14:(5,2),15:(5,4),16:(5,6),
                     17:(6,1),18:(6,3),19:(6,5),20:(6,7),
                     21:(7,0),22:(7,2),23:(7,4),24:(7,6)
                     }

#Initialize the piece[] objects
piece_list = [0 for i in range(24)]
#Place white pieces
for i in range(12):
    piece_list[i] = Piece(True,starting_loc_dict[i+1])
#Place black pieces
for i in range(12,24):
    piece_list[i] = Piece(False,starting_loc_dict[i+1])

#Print the initial board
board = [[0,0,0,0,0,0,0,0] for i in range(8)]

#------------------------------Game Functions--------------------------#

#Print the board and place the pieces
def print_board(board,piece_list):
    for row in range(8):
        for col in range(8):
            if (row+col)%2 == 0:
                board[row][col] = chr(9608)
            else:
                board[row][col] = " "
    for i in range(24):
        board[piece_list[i].location[0]][piece_list[i].location[1]] = piece_list[i]
    print("  01234567")
    for row in range(8):
        print(row,end=' ')
        for col in range(8):
            print(f"{board[row][col]}",end='')
        print(f" {row}",end='')
        print()
    print("  01234567")
    print()

#Update pieces positions on the board without printing it
def update_board(board, piece_list):
    for row in range(8):
        for col in range(8):
            if (row+col)%2 == 0:
                board[row][col] = chr(9608)
            else:
                board[row][col] = " "
    for i in range(24):
        board[piece_list[i].location[0]][piece_list[i].location[1]] = piece_list[i]

def player_input(board, must_jump, player_is_white):
    #Set a marker for whether the player jumped a piece or not
    jumped = False
    #Choose a piece to move
    while True:
        #Choose where to move from
        while True:
            if len(must_jump) == 1:
                print(f"{must_jump[0]} must jump this turn.")
                row_from = must_jump[0][0]
                col_from = must_jump[0][1]
                break
            #Choose a row to move from
            while True:
                try:
                    row_from = int(input("Input the row of the piece you'd like to move: "))
                except ValueError:
                    print("Please enter a number!")
                    continue
                if row_from < 0 or row_from > 7:
                    print("Please choose a number from 0 to 7")
                    continue
                else:
                    break
                
            #Choose a column to move from
            while True:
                try:
                    col_from = int(input("Input the column of the piece you'd like to move: "))
                except ValueError:
                    print("Please enter a number!")
                    continue
                if col_from < 0 or col_from > 7:
                    print("Please choose a number from 0 to 7")
                    continue
                else:
                    break
            
            #If a piece must jump, make sure that one of them has
            if len(must_jump) > 1:
                if (row_from, col_from) in must_jump:
                    #Make sure the row and column contain a piece of the player's team
                    if type(board[row_from][col_from]) == Piece:
                        if board[row_from][col_from].white_team == player_is_white:
                            break
                        else:
                            print("That square contains your opponent's piece! Try again.")
                    else:
                        print("That square doesn't have a piece on it! Try again.")
                else:
                    print(f"You have a piece that can jump! Please move {must_jump} instead")
            
            #If no piece has to jump
            else:
                #Make sure the row and column contain a piece of the player's team
                if type(board[row_from][col_from]) == Piece:
                    if board[row_from][col_from].white_team == player_is_white:
                        break
                    else:
                        print("That square contains your opponent's piece! Try again.")
                else:
                    print("That square doesn't have a piece on it! Try again.")
        
        #Choose a row to move to
        while True:
            try:
                row_to = int(input("Input the row of the square you'd like to move to: "))
            except ValueError:
                print("Please enter a number!")
                continue
            if row_to < 0 or row_to > 7:
                print("Please choose a number from 0 to 7")
                continue
            else:
                break
        
        #Choose a column to move to
        while True:
            try:
                col_to = int(input("Input the column of the square you'd like to move to: "))
            except ValueError:
                print("Please enter a number!")
                continue
            if col_to < 0 or col_to > 7:
                print("Please choose a number from 0 to 7")
                continue
            else:
                break
            
        #Make sure the row and column are a legal square to move to
        legal_moves = board[row_from][col_from].find_legal_moves(board)
        #If it is a legal move
        if (row_to, col_to) in legal_moves:
            #Set the pieces location
            board[row_from][col_from].location = (row_to, col_to)
            moved_piece = board[row_from][col_from]
            board[row_from][col_from] = ' '
            
            #If the piece jumped a piece, make it the jumped piece invisible and move it to (0,0)
            if abs(row_from-row_to) == 2:
                jumped_row = int((row_from+row_to)/2)
                jumped_col = int((col_from+col_to)/2)
                board[jumped_row][jumped_col].visible = False
                board[jumped_row][jumped_col].location = (0,0)
                board[jumped_row][jumped_col] = ' '
                jumped = True
                
            #If the piece reached the opposite edge, make it a king
            if moved_piece.white_team and moved_piece.location[0] == 7:
                moved_piece.king = True
            elif not moved_piece.white_team and moved_piece.location[0] == 0:
                moved_piece.king = True
            break
        else:
            print("That is not a legal move for that piece! Pick another space.")
            continue
    return board, moved_piece, jumped

#Take the player's turn
def player_move(board, piece_list, player_is_white, player_turn):
    
    #Make a list of the pieces that can jump and therefore one must
    must_jump = []
    piece_range = find_piece_range(player_is_white)
    for i in piece_range:
        piece_list[i].find_legal_moves(board)
        if piece_list[i].can_jump:
            print(f"{piece_list[i].location} can jump")
            must_jump.append(piece_list[i].location)
            
    #Get the player input and make the move
    board, moved_piece,jumped = player_input(board,must_jump,player_is_white)
    print_board(board,piece_list)
    
    #Check to see if the piece can jump again
    if jumped:
        moved_piece.find_legal_moves(board)
        while moved_piece.can_jump:
            must_jump = []
            must_jump.append(moved_piece.location)
            board, moved_piece,jumped = player_input(board,must_jump,player_is_white)
            print_board(board,piece_list)
            moved_piece.find_legal_moves(board)

    #Make it not the player's turn
    player_turn = not player_turn
    
    return board, piece_list, player_turn

def check_game_over(board, piece_list):
    
    #Check to see if either side won first
    
    #If there are no visible pieces for white, black wins
    for i in range(0,12):
        if piece_list[i].visible:
            break
    else:
        print("Black wins!")
        return True
    
    #If there are no legal moves for white, black wins
    for i in range(0,12):
        if piece_list[i].visible:
            legal_moves = piece_list[i].find_legal_moves(board)
            if legal_moves:
                break
    else:
        print("White has no legal moves. Black wins!")
        return True
    
    #If there are no visible pieces for black, white wins
    for i in range(12,24):
        if piece_list[i].visible:
            break
    else:
        print("White wins!")
        return True
    
    #If there are no legal moves for black, white wins
    for i in range(12,24):
        if piece_list[i].visible:
            legal_moves = piece_list[i].find_legal_moves(board)
            if legal_moves:
                break
    else:
        print("Black has no legal moves. White wins!")
        return True
    
    #Otherwise the game continues
    return False

#Find piece range depending on team
def find_piece_range(player_is_white):
    if player_is_white:
        return range(0,12)
    else:
        return range(12,24)

#Play a two player game
def play_two_player_game(board, piece_list, player_turn, player_is_white, game_over):
    
    #Print the board
    print_board(board,piece_list)
    
    #Turn loop
    while True:
        
        #Player 1's turn
        if player_turn:
            print("Player 1's Turn")
            board, piece_list, player_turn = player_move(board, piece_list, player_is_white, player_turn)
            if check_game_over(board, piece_list):
                break
            
        #Player 2's turn
        if not player_turn:
            print("Player 2's Turn")
            board, piece_list, player_turn = player_move(board, piece_list, not player_is_white, player_turn)
            if check_game_over(board, piece_list):
                break
            
def play_one_player_game(board, piece_list, player_turn, player_is_white, game_over):
    
    #Have the player decide the depth to which the computer will search each move
    while True:
        try:
            depth = int(input("Please input a depth for the computer searches (higher number = longer wait times). "))
        except ValueError:
            print("Please input an integer")
            continue
        if depth > 10 or depth < 0:
            print("Please input an integer from 0 to 10.")
            continue
        else:
            break
    
    #Print the board
    print_board(board,piece_list)
    
    #Turn loop
    while True:
        
        #Player 1's turn
        if player_turn:
            
            print("Player 1's Turn")
            
            #Have the player input a move, then make that move
            board, piece_list, player_turn, = player_move(board, piece_list, player_is_white, player_turn)

            #Check if the game is over
            if check_game_over(board,piece_list):
                break
            
        #Computer's turn
        if not player_turn:
            
            print("Computer's Turn")
            
            #Initialize counter for complexity of the board
            board_complexity = 0
            
            ###
            global move_count
            move_count = 0
            
            #Find board complexity finder
            for piece_index in range(24):
                if piece_list[piece_index].visible and not piece_list[piece_index].king:
                    board_complexity += 1
                elif piece_list[piece_index].visible and piece_list[piece_index].king:
                    board_complexity += 2
            
            ###
            print(f"Board complexity is: {board_complexity}")
            
            #Set added depth
            added_depth = set_added_depth(board_complexity)
            
            ###
            print(f"Added Depth is: {added_depth}")
                    
            #Store piece list
            stored_piece_list = copy.deepcopy(piece_list)
            
            #Find the best move
            best_piece, best_move, piece_list = find_best_move(board, piece_list, [], not player_is_white, depth, game_over)
            
            #Restore piece list and update board
            piece_list = stored_piece_list
            update_board(board, piece_list)
            
            #Find which piece was the best_piece
            for best_index in range(24):
                if piece_list[best_index].location == best_piece.location:
                    break
            
            #Print the move
            print(f"The computer moved from {piece_list[best_index].location} to {best_move}.")
            
            #Update the board
            update_board(board, piece_list)
            
            #Make that move
            board, piece_list[best_index], jumped = move_piece(board, best_piece, best_move)
            
            #If it jumped, give it the opportunity to jump again
            while jumped:
                jumped = False
                piece_list[best_index].find_legal_moves(board)
                if piece_list[best_index].can_jump:
                    #Store piece list
                    stored_piece_list = copy.deepcopy(piece_list)
                    
                    #Find the best move
                    best_piece, best_move, piece_list = find_best_move(board, piece_list, [best_index], not player_is_white, depth, game_over)
                    
                    #Restore piece list and update board
                    piece_list = stored_piece_list
                    update_board(board, piece_list)
                    
                    #Find which piece was the best_piece
                    for best_index in range(24):
                        if piece_list[best_index].location == best_piece.location:
                            break
                    
                    #Print the move
                    print(f"The computer moved from {piece_list[best_index].location} to {best_move}.")
                    
                    #Update the board
                    update_board(board, piece_list)
                    
                    #Make that move
                    board, piece_list[best_index], jumped = move_piece(board, best_piece, best_move)
                    
            ###
            print(f"The computer tested {move_count} moves")
                
            #Print out the new board
            print_board(board, piece_list)
            
            #Check if the game is over
            if check_game_over(board,piece_list):
                break
            
            #Change the turn
            player_turn = not player_turn

#----------------------------Computer Functions----------------------#

#Function for determining the extra depth the computer will search with
def set_added_depth(board_complexity):
    
    added_depth = 0
    
    if board_complexity < 12:
        added_depth += 1
    if board_complexity < 9:
        added_depth += 1
    if board_complexity < 7:
        added_depth += 1
    if board_complexity < 6:
        added_depth += 1
    if board_complexity < 5:
        added_depth += 1
    if board_complexity < 4:
        added_depth += 2
    if board_complexity < 3:
        added_depth += 3
    
    return added_depth
    
#Evaluate all possible moves for the computer to a certain depth
def mini_max(board, piece_list, jumped, piece_index, player_is_white, depth, game_over, alpha, beta):
    
    #Update_board
    for i in range(24):
        board[piece_list[i].location[0]][piece_list[i].location[1]] = piece_list[i]
    
    #Find the score of the board state
    score = eval_board(board, piece_list, player_is_white)
    
    #If the game is over, return the score
    game_over = check_game_over(board, piece_list)
    if game_over:
        return score
    
    #Check alpha-beta pruning
    if alpha < beta:
        #If a jump was just made, see if that piece can jump again
        if jumped:
            
            #Update the can_jump for the piece
            piece_list[piece_index].find_legal_moves(board)
            
        if jumped and piece_list[piece_index].can_jump:
            
            #Set the piece that must_jump to be the piece that just jumped
            must_jump_indeces = [piece_index]
            #Recursive function, will run once for each depth
            if depth > 0:
                score = eval_moves(board, piece_list, must_jump_indeces, jumped, player_is_white, depth - .1, game_over, alpha, beta)
        
        #If no piece jumped this turn, evaluate for the other player and decrease the depth
        else:
            if depth > 0:
                score = eval_moves(board, piece_list, [], jumped, not player_is_white, depth - 1, game_over, alpha, beta)
                
    ###
    #if alpha >= beta:
    #    print(f"Alpha {alpha} > Beta {beta}")
        
    #Once the depth is reached, return the score
    return score

def eval_moves(board, piece_list, must_jump_indeces, jumped, player_is_white, depth, game_over, alpha, beta):
    
    #Set a base for the best move based on whose turn it is
    if player_is_white:
        best_move_score = 5000
    else:
        best_move_score = -5000
    
    #Find which pieces are the computer's
    piece_range = find_piece_range(player_is_white)
    
    #If the player didn't make a jump earlier in the move, find which pieces must jump
    if not jumped:
        
        #For each piece
        for piece_index in piece_range:
            
            #Find the legal moves
            piece_list[piece_index].find_legal_moves(board)
            
            #If the piece can jump, add it to the must_jump list
            if piece_list[piece_index].can_jump:
                must_jump_indeces.append(piece_index)
    
    #If no piece must jump, proceed checkin all legal moves
    if len(must_jump_indeces) == 0:
        #Find all legal moves for a piece, play them out, then move on to the next piece
        piece_range = find_piece_range(player_is_white)
        for piece_index in piece_range:
            legal_moves = piece_list[piece_index].find_legal_moves(board)
            
            #If there are legal moves for that piece
            if legal_moves:
            
                #For each move, play it, then run mini_max function again
                for move in legal_moves:
                    
                    #Store the current board and piece information before making changes
                    stored_board = copy.deepcopy(board)
                    stored_piece_list = copy.deepcopy(piece_list)
                    
                    #Make the move
                    board, moved_piece, jumped = move_piece(board,piece_list[piece_index],move)

                    #Run the mini_max function again, with one less depth, for the other player, keeping track of the best move depending on whose turn it is
                    if player_is_white:
                        best_move_score = min(best_move_score, mini_max(board, piece_list, jumped, piece_index, player_is_white, depth, game_over, alpha, beta))
                        alpha = max(alpha, best_move_score)
                        ###
                        #print(f"Alpha is {alpha}")
                    else:
                        best_move_score = max(best_move_score, mini_max(board, piece_list, jumped, piece_index, player_is_white, depth, game_over, alpha, beta))
                        beta = min(beta, best_move_score)
                        ###
                        #print(f"Beta is {beta}")
                    
                    #Return the board to its original state
                    board = stored_board
                    piece_list = stored_piece_list
    
    #If a piece can jump, check only the legal moves for those pieces that can jump
    else:
        #For each piece that can jump
        for piece_index in must_jump_indeces:
            
            #Find the legal moves for that piece
            legal_moves = piece_list[piece_index].find_legal_moves(board)
            
            #Make each move then use the minimax function
            for move in legal_moves:
                
                #Store the current board and piece information before making changes
                stored_board = copy.deepcopy(board)
                stored_piece_list = copy.deepcopy(piece_list)
                
                #Make the move
                board, moved_piece, jumped = move_piece(board,piece_list[piece_index],move)
                
                #Run the mini_max function again, with one less depth, for the other player, keeping track of the best move depending on whose turn it is
                if player_is_white:
                    best_move_score = min(best_move_score, mini_max(board, piece_list, jumped, piece_index, not player_is_white, depth, game_over, alpha, beta))
                    alpha = max(alpha, best_move_score)
                    ###
                    #print(f"Alpha is {alpha}")
                else:
                    best_move_score = max(best_move_score, mini_max(board, piece_list, jumped, piece_index, not player_is_white, depth, game_over, alpha, beta))
                    beta = min(beta, best_move_score)
                    ###
                    #print(f"Beta is {beta}")
                    
                #Return the board to its original state
                board = stored_board
                piece_list = stored_piece_list
                    
    #Return the best score
    return best_move_score
        

def eval_board(board, piece_list, player_is_white):
    
    
    ###
    global move_count
    move_count += 1
    
    #Initialize the score and back row locations
    score = 0
    back_row_white = [(0,1), (0,3), (0,5), (0,7)]
    back_row_black = [(7,0), (7,2), (7,4), (7,6)]
    middle_squares = [(3,2), (4,3), (3,4), (4,5)]
    
    #Give the computer extra points for keeping pieces in the middle
    for index in range(0,12):
        if piece_list[index].location in middle_squares:
            score -= 8
    for index in range(12,24):
        if piece_list[index].location in middle_squares:
            score += 8
            
    #Give the computer/player extra points for keeping their pieces in the back row
    if computer_is_white:
        for index in [0,1,2,3]:
            if (not piece_list[index].king) and piece_list[index].location == back_row_white[index]:
                score += 10
        for index in [20,21,22,23]:
            if (not piece_list[index].king) and piece_list[index].location == back_row_black[index]:
                score -= 10
    
    #Give the computer/player extra points for keeping their pieces in the back row
    if not computer_is_white:
        for index in [0,1,2,3]:
            if (not piece_list[index].king) and piece_list[index].location == back_row_white[index]:
                score -= 10
        for index in [20,21,22,23]:
            if (not piece_list[index].king) and piece_list[index].location == back_row_black[index-20]:
                score += 10
    
    #Calculate the score based on the number of remaining pieces on each team
    for i in range(24):
        if piece_list[i].visible:
            if piece_list[i].white_team == computer_is_white and piece_list[i].king:
                score += 175
            elif piece_list[i].white_team != computer_is_white and piece_list[i].king:
                score -= 175
            elif piece_list[i].white_team == computer_is_white:
                score += 100
            elif piece_list[i].white_team != computer_is_white:
                score -= 100
    
    ###
    #print(f"Eval for move {move_count} is {score}")
    #Return score
    return score

def check_legal_moves(board, piece_list, piece_index, player_is_white, depth, game_over, legal_moves, best, best_move, best_piece):
    #For each move, evaluate the score given a depth
    for move in legal_moves:
        
        #Set alpha and beta bounds for alpha-beta pruning
        alpha = -5000
        beta = 5000
    
        #Store the board and piece_list
        stored_board = copy.deepcopy(board)
        stored_piece_list = copy.deepcopy(piece_list)
    
        #Make the move
        board, moved_piece, jumped = move_piece(board, piece_list[piece_index], move)
        
        #Find the score of the move using the mini_max function
        score = mini_max(board, piece_list, jumped, piece_index, player_is_white, depth, game_over, alpha, beta)
        #After checking the move, restore the board and piece_list
        board = stored_board
        piece_list = stored_piece_list
        
        #If the score is a tie for best, give a 1/3 chance it will replace it to vary moves
        if score == best:
            if randint(1,3) == 1:
                best = score
                best_move = copy.deepcopy(move)
                best_piece = copy.deepcopy(piece_list[piece_index])
                
        
        #If the move gives a new best score, make the piece the best_piece and the move the best_move to return to the computer
        if score > best:
            best = score
            best_move = copy.deepcopy(move)
            best_piece = copy.deepcopy(piece_list[piece_index])
            
        #Print loading bar
        print(chr(9608),end=' ')
        
    #Return the best_move and best_piece
    return best, best_move, best_piece
            
def find_best_move(board, piece_list, must_jump_indeces, player_is_white, depth, game_over):
    
    #Set a temporary best score
    best = -5000
            
    #Set a temporary best move
    best_move = None

    #Set a temporary best piece to move
    best_piece = None
    
    #Find which pieces are the computer's
    piece_range = find_piece_range(player_is_white)
    
    #If the piece has not already jumped
    if len(must_jump_indeces) == 0:
        #For each piece on the computer's team
        for piece_index in piece_range:
            
            #Update the can_jump for the piece
            piece_list[piece_index].find_legal_moves(board)
            
            #If the piece can jump, add it to the must_jump list
            if piece_list[piece_index].can_jump:
                print(f"{piece_list[piece_index].location} can jump")
                must_jump_indeces.append(piece_index)
    
    #If no piece can jump, find the best move
    if len(must_jump_indeces) == 0:
        
        #Print number of legal moves for loading bar
        legal_total = legal_moves_total(board, piece_list, player_is_white)
        print(f"{legal_total}: ", end='')
            
        for piece_index in piece_range:
            
            #Set a temporary best
            best_temp = -5000
            
            #Store the board and piece_list
            stored_board = copy.deepcopy(board)
            stored_piece_list = copy.deepcopy(piece_list)
            #Find the legal moves for all pieces on the computer's side
            
            legal_moves = piece_list[piece_index].find_legal_moves(board)
            
            #If the legal moves is not empty, check the score of the move
            if legal_moves:
                best_temp, best_move, best_piece = check_legal_moves(board, piece_list, piece_index, player_is_white, depth, game_over, legal_moves, best, best_move, best_piece)
            
            #If there is a new record
            if best_temp > best:
                best = best_temp

            #After checking the move, restore the board and piece_list
            board = stored_board
            piece_list = stored_piece_list
    
    #If a piece can jump
    else:
        
        #Print number of legal moves for loading bar
        print(f"{len(must_jump_indeces)}: ", end='')
        
        #For each piece that can jump
        for piece_index in must_jump_indeces:
            
            #Set a temporary best
            best_temp = -5000
            
            #Store the board and piece_list
            stored_board = copy.deepcopy(board)
            stored_piece_list = copy.deepcopy(piece_list)
            
            #Find the legal moves for that piece
            legal_moves = piece_list[piece_index].find_legal_moves(board)
            
            #For each legal move, use the minimax function
            best, best_move, best_piece = check_legal_moves(board, piece_list, piece_index, player_is_white, depth, game_over, legal_moves, best, best_move, best_piece)

            #After checking the move, restore the board and piece_list
            board = stored_board
            piece_list = stored_piece_list
            
    ###
    print(f"Computer score is: {best}")
    
    #Once all moves are considered, return the best one
    return best_piece, best_move, piece_list

            
def legal_moves_total(board, piece_list, player_is_white):
    piece_range = find_piece_range(player_is_white)
    legal_moves_length = 0
    for i in piece_range:
        legal_moves_length += len(piece_list[i].find_legal_moves(board))
    
    return legal_moves_length
        
    
def move_piece(board,moved_piece,move):
    
    #Set the froms and tos to be the piece location and the legal move location
    row_from = moved_piece.location[0]
    col_from = moved_piece.location[1]
    row_to = move[0]
    col_to = move[1]
    
    #Set the pieces new location (make the move)
    moved_piece.location = move
    board[row_from][col_from] = ' '
    
    #If the piece jumped a piece, make the jumped piece invisible and move it to (0,0)
    jumped = False
    if abs(row_from-row_to) == 2:
        jumped_row = int((row_from+row_to)/2)
        jumped_col = int((col_from+col_to)/2)
        board[jumped_row][jumped_col].visible = False
        board[jumped_row][jumped_col].location = (0,0)
        board[jumped_row][jumped_col] = ' '
        jumped = True
        
    #If the piece reached the opposite edge, make it a king
    if moved_piece.white_team and moved_piece.location[0] == 7:
        moved_piece.king = True
    elif not moved_piece.white_team and moved_piece.location[0] == 0:
        moved_piece.king = True

    return board, moved_piece, jumped

#---------------------------------Main-------------------------------#

if __name__ == "__main__":
    
    print("Welcome to the Checkers AI!")

    #Decide what type of game will be played
    while True:
        try:
            game_type = int(input("Please input a 1 for a one player game or a 2 for a two player game and hit enter. "))
        except ValueError:
            print("Please input an integer")
            continue
        if game_type > 2 or game_type < 1:
            print("Please input a 1 or 2.")
            continue
        else:
            break

    #Play a two player game if game type is 2
    if game_type == 2:
        play_two_player_game(board, piece_list, player_turn, player_is_white, game_over)

    #Play a one player game against the computer if game type is one
    if game_type == 1:
        play_one_player_game(board, piece_list, player_turn, player_is_white, game_over)

    
