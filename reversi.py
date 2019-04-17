# Copyright (c) 2019, William TANG <galaxyking0419@gmail.com>
from copy import deepcopy

# frequent used varibles
columns_map = {
	'a' : 1,
	'b' : 2,
	'c' : 3,
	'd' : 4,
	'e' : 5,
	'f' : 6,
	'g' : 7,
	'h' : 8
}

players_map = {
	1 : 'B',
	2 : 'W'
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

	# use insertion sort due to better performance
	for i in range(1, len(score_list)):
		for j in range(i, 0, -1):
			if score_list[j - 1][1] < score_list[j][1]:
				score_list[j], score_list[j - 1] = score_list[j - 1], score_list[j]
			else:
				break

	index = score_list[0][0]
	return valid_opts[index]
	

def prompt_to_place(board, player):
	pos = input("(%s) Enter the position to place your disk: " % (players_map[player]))
	#if the player want to quit, exit the program with code 1
	if pos == 'q':
		print("Thanks for playing the reversi.")
		exit(1)
	# phrase the position in the list
	pos = position(pos)

	if pos not in valid_moves(board, player):
		print("invalid move")
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
		print("%d |" % (i + 1), end = ' ')

		for j in range(8):
			if board[i][j] == 0:
				print("-", end = ' ')
			else:
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

	# if the index is out of range return false
	if not on_board([row, column]):
		return False

	# if there is a oppenent's chess beside your chess, continue checking
	if board[row][column] == your_oppenent(player):
		while on_board([row, column]):
			# if the current position is empty, return false
			if board[row][column] == 0:
				return False
			if board[row][column] == player:
				return True
			row += direct[0]
			column += direct[1]
	# if not, return false to accelerant the function
	else:
		return False
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

	# no valid move for both of players
	if valid_moves(board, 1) == [] and valid_moves(board, 2) == []:
		return board, 0
	return board, your_oppenent(player)


def position(pos):
	if len(pos) == 2 and pos[0] in "abcdefgh" and pos[1] in "1234567890":
		return [(int(pos[1]) - 1), (columns_map[pos[0]] - 1)]
	return None


def run_two_players():
	# initialize the borad and player
	player = 1
	game_board = new_board()

	# infinite loop to keep the game going
	while True:
		print_board(game_board)

		# pos must be a valid position
		pos = prompt_to_place(game_board, player)

		game_board, player = next_state(game_board, player, pos)

		if player == 0:
			finish_game(game_board)


def run_single_players():
	# initialize the borad and player
	counter = 1
	player = 1
	game_board = new_board()

	# infinite loop to keep the game going
	while True:
		print_board(game_board)

		# player place first
		if counter % 2 == 1:
			pos = prompt_to_place(game_board, player)
		else:
			pos = ai_place(game_board, player)

		game_board, player = next_state(game_board, player, pos)

		if player == 0:
			finish_game(game_board)
		
		counter += 1


# test zone
# uncomment them if you want to try examples in the assignment PDF
## (a)
#print(score(new_board()))
## (b)
#print(enclosing(new_board(), 1, (4, 5), (0, -1)))
#print(enclosing(new_board(), 1, (4, 5), (1, 1)))
## (c)
#print_board(next_state(new_board(), 1, (4, 5))[0])
#print(next_state(new_board(), 1, (4, 5))[1])
## (d)
#print(valid_moves(next_state(new_board(), 1, (4, 5))[0], 2))
## (e)
#print(position("e3"))
#print(position("Genghis Khan"))
# two players game & single player game
run_two_players()
#run_single_players()

# custom functions test zone
## ai_place()
#print(ai_place(new_board(), 2))


# The actual game starts from here, uncomment them if you want to play
#mode = input(
#"Welcome to the reversi!\n\
#enter 1 to play in single player mode\n\
#enter 2 to play in two players mode\n\
#Choose your mode: "
#)
#
#if mode == '1':
#	run_single_players()
#elif mode == '2':
#	run_two_players()
