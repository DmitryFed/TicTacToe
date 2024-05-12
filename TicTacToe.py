
from tabulate import tabulate  # type: ignore
import os
import random
import time 


class GameBoard:
    width  = 0
    height = 0
    board  = []
    delimiter_board = ' |'
    default_value = '_'
    def __init__(self,width,height):
        self.width = width
        self.height= height
        self.__setDefaultValues()
    
    def __setDefaultValues(self):
        num = 1
        default_value = self.delimiter_board + self.default_value
        for x in range(self.height):
          lst =[]
          for y in range(self.width):
              lst.append(str(num))
              num = num+1
          self.board.append(lst)

    def display(self):
       os.system("cls")
       print(tabulate(self.board,tablefmt="simple_grid"))

class TicTacToeBoard(GameBoard):
    def __init__(self,size):
        super().__init__(width = size,height = size)
         
class Player:
    name = ''
    sign = ''
    winner = False
    def __init__(self,name,sign):
        self.name = name 
        self.sign = sign
    def greetings(self):
        print(f"{self.name} sign: {self.sign}")
        
class Game:
    game_board = None
    __players = []
    def __init__(self,board,players=[]):
        self.__players.extend(players)        
        self.game_board = board 

class TicTacToeWinConditions:
    conditions = {}
    list_conditions = []

    def __init__(self,size):
        self.__setMainDiagonalCondition(size)
        self.__setSideDiagonalCondition(size)
        self.__setColumnsCondition(size)
        self.__setRowsCondition(size)
    
    def __setMainDiagonalCondition(self,size):
        index = 0
        mainDiagset = set()
        mainDiagset.add(index)
        for offsetCount in range(size-1):
            index+=size+1
            mainDiagset.add(index)
        self.list_conditions.append(mainDiagset)
    def __setSideDiagonalCondition(self,size):
        index = size - 1
        sideDiagset = set()
        sideDiagset.add(index)
        for offsetCount in range(size-1):
            index+= size - 1
            sideDiagset.add(index)
        self.list_conditions.append(sideDiagset)

    def getColumnNumber(self,size,index):
         colNumber = size if index%size == 0 else index%size 
         colNumber = colNumber - 1
         return colNumber

    def getRowNumber(self,size,index):
         return int(index/size)
         
    def __setColumnsCondition(self,size):
        listOfSets = []
        for x in range(size):
            colset = set()
            listOfSets.append(colset)
        for i in range(size**2):
           colnumber = self.getColumnNumber(size,i)
           listOfSets[colnumber].add(i)
        self.list_conditions.extend(listOfSets)
           
    def __setRowsCondition(self,size):
       listOfRows = []
       for j in range(size):
           rowset = set()
           listOfRows.append(rowset)
       for i in range(size**2):
          rowNumber = self.getRowNumber(size,i)
          listOfRows[rowNumber].add(i)
       self.list_conditions.extend(listOfRows)

class TicTacToeMoves:
    moves = {}

    def setMovesKey(self,key):
        if key not in self.moves:
            self.moves[key] = set()

    def addmove(self,key,value): 
        self.setMovesKey(key)
        self.moves[key].add(value)
 
class TicTacToe(Game):
    
    player_one = None 
    player_two = None
    moves = TicTacToeMoves()
    game_result = 0 
    win_conditions = None
    total_moves = []

    def __init__(self,first_player,second_player,board):
        super().__init__(board)
        self.win_conditions = TicTacToeWinConditions(board.width)
        self.player_one = first_player
        self.player_two = second_player

    def MakeMove(self,player,positionNumber):
        coords = CastCoords.NumberToCoords(positionNumber,self.game_board.width)
        x = coords[0]
        y = coords[1]
        self.game_board.board[x][y] = player.sign 
        self.addmove(player,positionNumber)
        player.winner = self.CheckWinner(player)
        self.DisplayMoves()
    
    def addmove(self,player,position_number):
        self.total_moves.append(position_number)
        self.moves.addmove(player.name,position_number)

    def set_game_result(self):
        if self.player_one.winner:
            self.game_result = 1
        if self.player_two.winner:
            self.game_result = 2
        if len(self.total_moves) == self.game_board.width**2 and not self.player_one.winner and not self.player_two.winner:
            self.game_result = 3

    

    def CheckUsedCell(self,number):
      return number in self.total_moves
                
    def DisplayMoves(self):
        for key in self.moves.moves:
            print(key,": ",self.moves.moves[key])

    def CheckWinner(self,playa):
        moves = self.moves.moves[playa.name]
        for winset in self.win_conditions.list_conditions:
            if len(winset - moves) == 0: 
                playa.winner = True
                break
        self.set_game_result()
        return

    def is_winner(self,player):
        return player.winner

          
class CastCoords:
    def CoordsToNumber(x,y,size):
        return x * size + y 

    def NumberToCoords(number,size):
        y = number % size 
        x = int((number-y)/size)
        return (x,y)



class Strategy:
    current_vector = []
    current_vector_index = -1

    def search_defence_move(self,opponent_moves,winVectors,selfmoves):
         defence_move = -1 
         for vector in winVectors:
            if len(vector - set(opponent_moves)) == 1 and vector.difference(set(opponent_moves)).pop() not in selfmoves: 
               defence_move = vector.difference(set(opponent_moves)).pop()
               break
         return defence_move
    
    def search_win_move(self,opponent_moves,winVectors,selfmoves):
        win_move =-1 
        for vector in winVectors:
            if  len(vector - set(selfmoves)) == 1 and vector.difference(set(selfmoves)).pop() not in opponent_moves:
                win_move = vector.difference(set(selfmoves)).pop() 
                break
        return win_move

    def search_free_vector(self,opponent_moves,winVectors):
        for vector in winVectors:
            if len(set(vector)-opponent_moves) == len(vector):
                return list(vector)
        return []
    def set_to_start_vector_index(self):
        self.current_vector_index = 0 

    def next(self):
        if len(self.current_vector) - 1 > self.current_vector_index:
            self.current_vector_index += 1
    
    def reset_vector(self):
        self.current_vector = set()
        self.current_vector_index = -1

    def get_defence_move(self,opponent_moves,winVectors,selfmoves):
        defence_move = self.search_defence_move(opponent_moves,winVectors,selfmoves)
        return defence_move
    
    def is_empty_vector(self,vector):
        return vector == None or len(vector) == 0
    
    def free_moves(self,opponent_moves,selfmoves):
        return set(set(self.current_vector) - set(selfmoves)).difference(set(opponent_moves))

    def get_next_vector_move(self,opponent_moves,selfmoves,winvectors,boardsize):
        if self.is_empty_vector(self.free_moves(opponent_moves,selfmoves)):
           return self.random_move(boardsize,opponent_moves|selfmoves)

        return self.free_moves(opponent_moves,selfmoves).pop()

        
    def init_vector(self,opponent_moves,winVectors):
        self.search_free_vector(opponent_moves,winVectors)

    def random_move(self,board_size,moves):
        allmoves = list(range(board_size**2 - 1))
        return set(allmoves).difference(moves).pop()
       
          
    def is_opponent_move(self,opponent_moves):
        return self.current_vector[self.current_vector_index] in opponent_moves

    def get_move(self,opponent_moves,winVectors,selfmoves,boardsize):
        current_move = self.search_win_move(opponent_moves,winVectors,selfmoves)
        if current_move != -1: return current_move
        else:
            current_move = self.get_defence_move(opponent_moves,winVectors,selfmoves)
            if current_move in selfmoves: current_move = -1
            if current_move == -1:
                if self.is_empty_vector(self.current_vector) or self.is_opponent_move(opponent_moves):
                    self.current_vector = self.search_free_vector(opponent_moves,winVectors)
                    current_move = self.get_next_vector_move(opponent_moves,selfmoves,winVectors,boardsize)             
                else:
                    current_move = self.get_next_vector_move(opponent_moves,selfmoves,winVectors,boardsize)  
        return current_move     

   
class Bot(Player):
    vectors = []
    strategy = Strategy()

    def __init__(self, name, sign):
        super().__init__(name, sign)

    def set_vectors(self,sets):
        self.vectors = sets
    
    def change_vector(self, new_vector):
        self.current_vector = new_vector
    
    def get_move(self,opponent_moves,winVectors,selfmoves,boardsize):
          return  self.strategy.get_move(opponent_moves,winVectors,selfmoves,boardsize)

    def get_random_move(self,board_size,moves):
       return self.strategy.random_move(board_size,moves)

def main():

    player1 = Bot("Probe","X")
    player2 = Player("—оздатель","0")

    players = [player1,player2]
    
    current_player_move = 0
    current_player = None
    board_size = 3
    board = TicTacToeBoard(board_size)
    game  = TicTacToe(player1,player2,board)
    board.display()
    game.moves.setMovesKey(player1.name)
    game.moves.setMovesKey(player2.name)
    player_moves = [game.moves.moves[player1.name],game.moves.moves[player2.name]]
    total_moves = game.total_moves
    current_player = players[current_player_move]

    winVectors = game.win_conditions
  
    while(game.game_result == 0):
        
        current_player_move = abs(current_player_move-1)

        if type(current_player) is not Bot:
            print("¬ведите номер €чейки")
            number = int(input()) - 1
        else:
            number = current_player.get_move(player_moves[current_player_move],winVectors.list_conditions,player_moves[abs(current_player_move-1)],board_size)
        
        game.MakeMove(current_player,number)
        board.display()
        game.DisplayMoves()
        time.sleep(1)
        current_player = players[current_player_move]
    if game.game_result == 3:
        print("It's a draw")
    else:
        print("winner is: " ,players[game.game_result-1].name)
    
main() 

