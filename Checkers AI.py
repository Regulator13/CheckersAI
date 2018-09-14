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

#Classes
class Piece():
    
    def __init__(self, white_team ,location ,king=False ,can_jump = False, visible = True):
        '''
        The Piece object handles all pieces on the board.
        white_team -- True if team is white
                location -- tuple (row,col)
        king -- True if the piece is a king
        can_jump -- True if the piece can make a legal jump
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

#Dicitonary for starting piece locations
starting_loc_dict = {1:(0,1),2:(0,3),3:(0,5),4:(0,7),
                     5:(1,0),6:(1,2),7:(1,4),8:(1,6),
                     9:(2,1),10:(2,3),11:(2,5),12:(2,7),
                     13:(5,0),14:(5,2),15:(5,4),16:(5,6),
                     17:(6,1),18:(6,3),19:(6,5),20:(6,7),
                     21:(7,0),22:(7,2),23:(7,4),24:(7,6)
                     }

#Initialize the piece[] objects
piece = [0 for i in range(24)]
#Place white pieces
for i in range(12):
    piece[i] = Piece(True,starting_loc_dict[i+1])
#Place black pieces
for i in range(12,24):
    piece[i] = Piece(False,starting_loc_dict[i+1])

#Print the initial board
board = [[0,0,0,0,0,0,0,0] for i in range(8)]
for row in range(8):
    for col in range(8):
        if (row+col)%2 == 0:
            board[row][col] = chr(9608)
        else:
            board[row][col] = " "

#---------------------------------Functions--------------------------#

#Print the board and place the pieces
def print_board(board,piece):
    for i in range(24):
        board[piece[i].location[0]][piece[i].location[1]] = piece[i]
    print("  01234567")
    for row in range(8):
        print(row,end=' ')
        for col in range(8):
            print(f"{board[row][col]}",end='')
        print(f" {row}",end='')
        print()
    print("  01234567")
    print()

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
def player_move(board, player_is_white, player_turn):
    #Make a list of the pieces that can jump and therefore one must
    must_jump = []
    if player_is_white:
        piece_range = range(0,12)
    else:
        piece_range = range(12,24)
    for i in piece_range:
        piece[i].find_legal_moves(board)
        if piece[i].can_jump:
            print(f"{piece[i].location} can jump")
            must_jump.append(piece[i].location)
    board, moved_piece,jumped = player_input(board,must_jump,player_is_white)
    print_board(board,piece)
    #Check to see if the piece can jump again
    if jumped:
        moved_piece.find_legal_moves(board)
        while moved_piece.can_jump:
            must_jump = []
            must_jump.append(moved_piece.location)
            board, moved_piece,jumped = player_input(board,must_jump,player_is_white)
            print_board(board,piece)
            moved_piece.find_legal_moves(board)
    player_turn = not player_turn
    return board, player_turn

def game_over(board,piece):
    
    #Check to see if either side won first
    
    #If there are no visible pieces for white, black wins
    for i in range(0,12):
        if piece[i].visible:
            break
    else:
        print("Black wins!")
        return True
    
    #If there are no legal moves for white, black wins
    for i in range(0,12):
        if piece[i].visible:
            legal_moves = piece[i].find_legal_moves(board)
            if legal_moves:
                break
    else:
        print("Black wins!")
        return True
    
    #If there are no visible pieces for black, white wins
    for i in range(12,24):
        if piece[i].visible:
            break
    else:
        print("White wins!")
        return True
    
    #If there are no legal moves for black, white wins
    for i in range(12,24):
        if piece[i].visible:
            legal_moves = piece[i].find_legal_moves(board)
            if legal_moves:
                break
    else:
        print("White wins!")
        return True
    
    #Otherwise the game continues
    return False
            
#---------------------------------Main-------------------------------#

print_board(board,piece)
print("Welcome to the Checkers AI!")
#Player's turn
while True:
    if player_turn:
        print("Player 1's Turn")
        board, player_turn = player_move(board,player_is_white,player_turn)
        if game_over(board,piece):
            break
    #Other turn
    if not player_turn:
        print("Player 2's Turn")
        board, player_turn = player_move(board,not player_is_white,player_turn)
        if game_over(board,piece):
            break
        
