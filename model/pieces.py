import copy
from view import print_board
def around(position):
    """" return six point around the position as a list """
    x, y = position
    around_point = [(x + 1, y)]
    if y % 2 == 0:
        around_point.append((x, y + 1))
        around_point.append((x - 1, y + 1))
        around_point.append((x - 1, y))
        around_point.append((x - 1, y - 1))
        around_point.append((x, y - 1))
    else:
        around_point.append((x + 1, y + 1))
        around_point.append((x, y + 1))
        around_point.append((x - 1, y))
        around_point.append((x, y - 1))
        around_point.append((x + 1, y - 1))
    return around_point


def initial_condition_for_move(piece, board):
    new_board = copy.deepcopy(board)

    x, y = new_board.pieces.get(piece)  # old position of the piece

    # only upper piece can move
    if not new_board.board[y][x][-1] == piece:
        return False

    new_board.board[y][x].remove(piece)
    del new_board.pieces[piece]

    # if after movement node isn't empty continuity is ok
    if new_board.board[y][x] == []:
        if not check_continuity(new_board, (x, y)):
            return False

    return new_board



def can_move(piece, des_position, board, continuity=True):
    """ check that movement is possible based on piece role """
    # it can be 'A', 'B', 'L', 'Q', 'S'
    piece_role = piece[1]

    new_board = None
    if continuity:
        new_board = initial_condition_for_move(piece, board)
        if new_board is False:
            return False

    x, y = board.pieces.get(piece)

    if piece_role == 'A':  # Ant
        return ant_move(des_position, (x, y), new_board, piece)
    elif piece_role == 'B':  # Beetle
        return beetle_move(des_position, (x, y), new_board, piece)
    elif piece_role == 'L':  # Locust
        return locust_move(des_position, (x, y), board)
    elif piece_role == 'Q':  # Queen
        return queen_move(des_position, (x, y), new_board, piece)
    elif piece_role == 'S':  # Spider
        return spider_move(des_position, (x, y), new_board, piece)
    else:
        print("something wrong")
        return False


def check_continuity(board, position):
    new_board = copy.deepcopy(board)
    traverse(position, new_board,True)
    if len(new_board.pieces) == 0:
        return True
    return False


def traverse(position, board, first=False):
    arounds = around(position)
    for neighbour in arounds:
        x, y = neighbour
        try:
            pieces = board.board[y][x]
            board.board[y][x] = []
            if not pieces == []:
                for piece in pieces:
                    del board.pieces[piece]
                traverse(neighbour, board)
                if first:
                    break
        except:
            pass


def ant_move(des_position, position, board, piece):
    x, y = des_position
    if board.board[y][x] == []:
        if check_surrounding(des_position, board, piece) \
                and check_surrounding(position, board, piece):
            return True
    return False


def beetle_move(des_position, position, board, piece):
    x, y = des_position
    if des_position in around(position):
        if board.board[y][x] == []:
            if check_surrounding(des_position, board, piece) \
                    and check_surrounding(position, board, piece):
                return True
        else:
            return True
    return False


def locust_move(des_position, position, board):
    pos_x, pos_y = position
    x, y = position
    des_x, des_y = des_position

    # locust can't go to his arounds
    if abs(x - des_x) <= 1 and \
            abs(y - des_y) <= 1:
        return False

    # find move direction
    y_direction = ''
    x_direction = ''
    if y == des_y:
        y_direction = 'no'
    elif y < des_y:
        y_direction = 'r'
    else:
        y_direction = 'l'

    if x == des_x:
        return False
    elif x < des_x:
        x_direction = 'r'
    elif x > des_x:
        x_direction = 'l'

    # move position to des_position Loop
    
    if y_direction == 'no' and x_direction == 'r':
        while True:
            if y == des_y and x == des_x:
                return True
            if board.board[y][x] == []:
                return False
            x += 1
            if x > des_x:
                return False
    
    elif y_direction == 'no' and x_direction == 'l':
        while True:
            if y == des_y and x == des_x:
                return True
            if board.board[y][x] == []:
                return False
            x -= 1
            if x < des_x:
                return False
            
    elif y_direction == 'r' and x_direction == 'r':
        while True:
            if y == des_y and x == des_x:
                return True
            if board.board[y][x] == []:
                return False
            y += 1
            if y > des_y:
                return False
            if y % 2 == 0:
                x += 1
                if x > des_x:
                    return False
                
    elif y_direction == 'r' and x_direction == 'l':
        while True:
            if y == des_y and x == des_x:
                return True
            if board.board[y][x] == []:
                return False
            y += 1
            if y > des_y:
                return False
            if y % 2 == 1:
                x -= 1
                if x < des_x:
                    return False    
                
    elif y_direction == 'l' and x_direction == 'r':
        while True:
            if y == des_y and x == des_x:
                return True
            if board.board[y][x] == []:
                return False
            y -= 1
            if y < des_y:
                return False
            if y % 2 == 0:
                x += 1
                if x > des_x:
                    return False
    
    elif y_direction == 'l' and x_direction == 'l':
        while True:
            if y == des_y and x == des_x:
                return True
            if board.board[y][x] == []:
                return False
            y -= 1
            if y < des_y:
                return False
            if y % 2 == 1:
                x -= 1
                if x < des_x:
                    return False           
    
    else:
        return "I think Code is not True :)"


def queen_move(des_position, position, board, piece):
    x, y = des_position
    if des_position in around(position):
        if board.board[y][x] == []:
            if check_surrounding(des_position, board, piece) \
                    and check_surrounding(position, board, piece):
                return True
    return False


def spider_move(des_position, position, board, piece, all_position=False):
    result = []
    arounds = around(position)
    if check_surrounding(position, board, piece):
        for around_point in arounds:
            if spider_checking(around_point, board, piece):
                first = around_point
                arounds_first = around(first)

                arounds_first = [number for number in arounds_first if number[0] >= 0 and number[1] >= 0]
                for around_first in arounds_first:
                    if spider_checking(around_first, board, piece) \
                            and not around_first == position:
                        arounds_second = around(around_first)
                        second = around_first

                        arounds_second = [number for number in arounds_second if number[0] >= 0 and number[1] >= 0]
                        for around_second in arounds_second:
                            if spider_checking(around_second, board, piece) and not around_second == first and not around_second == second and not around_second == position:
                                result.append(around_second)

    return result if all_position else des_position in result


def spider_checking(des_position, board, piece):
    x, y = des_position

    try:
        if board.board[y][x] == []:
            if check_surrounding(des_position, board, piece):
                around_des = around(des_position)
                for point in around_des:
                    try:
                        xx, yy = point
                        if not board.board[yy][xx] == []:
                            return True
                    except:
                        pass
    except:
        pass
    return False


def check_surrounding(position, board, piece):
    arounds = around(position)
    for i in range(0, 6):
        try:
            x, y = arounds[i]
            if board.board[y][x] == [] or board.board[y][x][-1] == piece:
                if i < 5:
                    x, y = arounds[i + 1]
                else:
                    x, y = arounds[0]
                if board.board[y][x] == [] or board.board[y][x][-1] == piece:
                    return True
        except:
            pass
    return False


def piece_naming(piece):
    if piece[1] == 'Q':
        return "queen"
    if piece[1] == 'B':
        return "beetle"
    if piece[1] == 'S':
        return "spider"
    if piece[1] == 'L':
        return "locust"
    if piece[1] == 'A':
        return "ant"

