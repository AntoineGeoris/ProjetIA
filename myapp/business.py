from models import GameBoard

table = [
    ['1','0','0','0','0'],
    ['0','0','0','0','0'],
    ['0','0','0','0','0'],
    ['0','0','0','0','0'],
    ['0','0','0','0','2']
]

game_board_state_to_str = lambda cells : "" if len(cells) == 0 else "".join(cells[0]) + game_board_state_to_str(cells[1:])

def  game_board_state_from_str(string):
    table = []
    for i in range(1,6):
        line = []
        for y in range((i - 1) * 5, i * 5):
            line.append(string[y])
        table.append(line)
    return table

def move_allowed(game_state, player_pos, move):
    line = player_pos[0]
    column = player_pos[1]

    if move == "left":
        return column - 1 >= 0 and game_state[line][column - 1] == '0'
    if move == "right":
        return column + 1 >= 0 and game_state[line][column + 1] == '0'
    if move == "down":
        return line + 1 >= 0 and game_state[line + 1][column] == '0'
    
    return line - 1 >= 0 and game_state[line - 1][column] == '0'

def move(game_state, player_pos, move, num_player):
    if move_allowed:
        line = player_pos[0]
        column = player_pos[1]

        if move == "left":
            game_state[line][column - 1] = num_player
        elif move == "right":
            game_state[line][column + 1] = num_player
        elif move == "down":
            game_state[line + 1][column] = num_player
        else:
            game_state[line - 1][column] = num_player
    
    