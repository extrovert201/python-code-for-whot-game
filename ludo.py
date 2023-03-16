import random

class Token:
    def __init__(self, player, id):
        self.player = player
        self.id = id
        self.current_tile = None
        self.start_position = StartPosition(player)
        self.is_home = False
        
    def can_move(self):
        # Tokens can only enter the home stretch by exact roll of the die
        if self.is_home:
            return False
        
        # Tokens in the start position can only move if a 6 is rolled
        if self.current_tile is None:
            if self.player.current_roll == 6:
                return True
            else:
                return False
        
        # Tokens in the main board can move if the sum of the current roll and their current tile number is less than or equal to 56
        if self.current_tile.number + self.player.current_roll <= 56:
            return True
        else:
            return False
        
    def move(self):
        if self.current_tile is None:
            self.current_tile = self.start_position.start_tile
            self.start_position.remove_token(self)
        else:
            self.current_tile.remove_token(self)
            new_tile_number = self.current_tile.number + self.player.current_roll
            if new_tile_number > 56:
                return
            self.current_tile = self.current_tile.get_next_token(new_tile_number)
            
            if self.current_tile.is_home:
                self.is_home = True
        
        self.current_tile.add_token(self)
        
        
class Tile:
    def __init__(self, number):
        self.number = number
        self.tokens = []
        self.is_home = False
        
    def add_token(self, token):
        self.tokens.append(token)
        
    def remove_token(self, token):
        self.tokens.remove(token)
        
    def get_next_token(self, steps):
        if steps == 0:
            return self
        else:
            next_tile_number = self.number + 1
            if next_tile_number in HOME_ROW_NUMBERS:
                return self.get_next_token(steps - 1).get_home_row_tile(next_tile_number)
            else:
                return BOARD[next_tile_number % BOARD_SIZE]
            
    def get_home_row_tile(self, home_row_number):
        for tile in HOME_ROWS[self.tokens[0].player.color]:
            if tile.number == home_row_number:
                return tile
            
        
class StartPosition:
    def __init__(self, player):
        self.player = player
        self.start_tile = START_TILES[player.color]
        self.tokens = [Token(player, i) for i in range(NUMBER_OF_TOKENS)]
        
    def remove_token(self, token):
        self.tokens.remove(token)
        
        
class Player:
    def __init__(self, color):
        self.color = color
        self.tokens = [Token(self, i) for i in range(NUMBER_OF_TOKENS)]
        self.current_roll = 0
        self.won_tokens = 0
        
    def roll_dice(self):
        self.current_roll = random.randint(1, 6)
        
    def play_turn(self):
        for token in self.tokens:
            if token.can_move():
                token.move()
                break
                
    def check_for_winning_tokens(self):
        for token in self.tokens:
            if token.is_home:
                self.won_tokens += 1
                
    def has_won(self):
        return self.won_tokens == NUMBER_OF_TOKENS
    
    
START_TILES = {
    'red': Tile(1),
    'green': Tile(14),
    'blue': Tile(27),
    'yellow': Tile(40)
}

HOME_ROW_NUMBERS = [1, 8, 14, 21, 27, 34, 40]
BOARD_SIZE = 56

BOARD = [Tile(i+1) for i in range(BOARD_SIZE)]

for i in range(1, 53, 6):
for j in range(6):
BOARD[i+j].is_home = True

HOME_ROWS = {
'red': [BOARD[i] for i in range(0, 7)],
'green': [BOARD[i] for i in range(13, 20)],
'blue': [BOARD[i] for i in range(26, 33)],
'yellow': [BOARD[i] for i in range(39, 46)]
}

NUMBER_OF_TOKENS = 4

PLAYERS = [Player(color) for color in ['red', 'green', 'blue', 'yellow']]

while True:
for player in PLAYERS:
player.roll_dice()
player.play_turn()
player.check_for_winning_tokens()
if player.has_won():
print(f"{player.color.capitalize()} player has won the game!")
exit()
