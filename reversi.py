# Copyright (c) 2019, William TANG <galaxyking0419@gmail.com>
# necessary modules
from copy import deepcopy
from time import sleep
from random import choice

# global varibles
players_map = {
	0: '-',
	1: 'B',
	2: 'W'
}

direction_list = [
	[1, 1],
	[0, 1],
	[1, 0],
	[0, -1],
	[-1, 0],
	[1, -1],
	[-1, 1],
	[-1, -1]
]

random_sentences = [
	"Emmm, interesting...",
	"Let me think for a while...",
	"Hold my beer",
	"Aha! You are dead!"
]

# custom functions
def your_oppenent(player):
	if player == 1:
		return 2
	return 1


def on_board(pos):
	return (pos[0] >= 0 and pos[0] <= 7) and (pos[1] >= 0 and pos[1] <= 7)


def ai_place(board, player):
	score_list = []
	counter = 0
	valid_opts = valid_moves(board, player)

	for opt in valid_opts:
		board_next = deepcopy(board)
		# append the index to the score list which make it easier to retrive the position
		current_score = score(board_next)[1]
		score_list.append([counter, score(next_state(board_next, player, opt)[0])[1] - current_score])
		counter += 1

	# sort in descending order
	sorted(score_list, key=lambda score: score_list[1], reverse=True)
	index = score_list[0][0]
	return valid_opts[index]


def prompt_to_place(board, player):
	pos = input("(%s) Enter the position to place your disk: " % (players_map[player]))

	#if the player want to quit, exit the program with code 1
	if pos == 'q':
		print("Thanks for playing my Reversi.")
		exit(0)

	# phrase the position in the list
	pos = position(pos)

	if pos not in valid_moves(board, player):
		print("Come on, don't mess up with me.")
		return prompt_to_place(board, player)
	return pos


def finish_game(board):
	black_score, white_score = score(board)

	print("The game has finished")
	print("Black Score: ", black_score)
	print("White Score: ", white_score)

	# compare to claim the winner
	if black_score > white_score:
		print("Black Wins!")
	elif black_score == white_score:
		print("Draw!")
	else:
		print("White Wins!")
	exit(0)


# functions required in the task sheet
def new_board():
	board_list = [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 2, 1, 0, 0, 0],
		[0, 0, 0, 1, 2, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0]
	]
	return board_list


def print_board(board):
	for i in range(8):
		# print row number before each row
		print("%d" % (i + 1), end = ' | ')

		for j in range(8):
			print(players_map[board[i][j]], end = ' ')

		# print the socre board on the right	
		if i == 3:
			print("\tBlack Score: ", score(board)[0], end = '')
		elif i == 5:
			print("\tWhite Score: ", score(board)[1], end = '')
		print()

	# print column character at the end of graph
	print("--------------------")
	print("    a b c d e f g h")


def score(board):
	black_score = 0
	white_score = 0
	for i in range(8):
		for j in range(8):
			if board[i][j] == 1:
				black_score += 1
			elif board[i][j] == 2:
				white_score += 1
	return black_score, white_score


def enclosing(board, player, pos, direct):
	row = pos[0] + direct[0]
	column = pos[1] + direct[1]

	# if there is a oppenent's chess beside your chess, continue checking
	while on_board([row, column]) and board[row][column] == your_oppenent(player):
		if on_board([row+direct[0], column+direct[1]]) and board[row+direct[0]][column+direct[1]] == player:
			return True
		row += direct[0]
		column += direct[1]
	# default to false
	return False


def valid_moves(board, player):
	moves_list = []

	# iterate each empty position to check if it will enclose certain direction of line
	for i in range(8):
		for j in range(8):
			for direction in direction_list:
				if board[i][j] == 0 and enclosing(board, player, [i, j], direction):
					moves_list.append([i, j])
					# exit the direction loop if find one eligible position
					break
	return moves_list


def next_state(board, player, pos):
	# if there is no valid move for both of players
	if valid_moves(board, 1) == [] and valid_moves(board, 2) == []:
		return board, 0

	board[pos[0]][pos[1]] = player
	for direction in direction_list:
		# copy the value of direction list in case of varible changes
		direction_next = direction[:]
		if enclosing(board, player, pos, direction) == True:
			while board[pos[0] + direction_next[0]][pos[1] + direction_next[1]] != player:
				# change all opponent's chess to your's
				board[pos[0] + direction_next[0]][pos[1] + direction_next[1]] = player
				direction_next[0] += direction[0]
				direction_next[1] += direction[1]
	return board, your_oppenent(player)


def position(pos):
	columns_map = {
		'a': 1,
		'b': 2,
		'c': 3,
		'd': 4,
		'e': 5,
		'f': 6,
		'g': 7,
		'h': 8
	}
	if len(pos) == 2 and pos[0] in "abcdefgh" and pos[1] in "1234567890":
		return [(int(pos[1]) - 1), (columns_map[pos[0]] - 1)]
	return None


def run_two_players():
	# initialize the borad and player
	player = 1
	game_board = new_board()

	# while the player is 1 or 2 keep the game going
	while player != 0:
		print_board(game_board)

		# pos must be a valid position
		pos = prompt_to_place(game_board, player)

		game_board, player = next_state(game_board, player, pos)

	# finish game once the player is 0
	finish_game(game_board)


def run_single_players():
	# initialize the borad and player
	player = 1
	game_board = new_board()

	# while the player is 1 or 2 keep the game going
	while player != 0:
		print_board(game_board)

		# player place first
		if player == 1:
			pos = prompt_to_place(game_board, player)
		else:
			print(choice(random_sentences))
			sleep(2)
			pos = ai_place(game_board, player)

		game_board, player = next_state(game_board, player, pos)
	# finish game once the player is 0
	finish_game(game_board)

# main program
if __name__ == "__main__":
	mode = input("Welcome to the reversi!\nenter 1 to play in single player mode\nenter 2 to play in two players mode\nChoose your mode: ")
	if mode == '1':
		run_single_players()
	elif mode == '2':
		run_two_players()
