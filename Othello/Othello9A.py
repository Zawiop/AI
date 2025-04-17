
import sys; args = sys.argv[1:]
import math

def input():
    board_str = args[0]
    n = len(board_str)
    if len(args) >=2:
        width = int(args[1])
    else:
        start = math.ceil(math.sqrt(n))
        for d in range(start, n+1):
            if n % d == 0:
                width = d
                break
    height = n // width
    return board_str, width, height

def print2D(board, width):
    height = len(board) // width  
    for i in range(height):
        print("".join(str(board[i * width + j]) for j in range(width)))

def makeInto2D(board_str, width, height):
    return [ list(board_str[i*width:(i+1)*width]) for i in range(height) ]

def boardToStr(board):
    return ''.join(''.join(row) for row in board)


def identity(board):
    return [row[:] for row in board]

def rotate90(board):
    height = len(board)
    width = len(board[0])
    new_board = []
    for i in range(width):
        new_row = []
        for j in range(height):
            new_row.append(board[height - 1 - j][i])
        new_board.append(new_row)
    return new_board

def rotate180(board):
    
    return rotate90(rotate90(board))

def rotate270(board):
    return rotate90(rotate90(rotate90(board)))

def horizontalR(board):
    return [ list(reversed(row)) for row in board ]

def verticalR(board):
    return rotate180(horizontalR(board))

def rightToLeft(board): #diagonal 1
    
    height = len(board)
    width = len(board[0])
    new_board = []
    for i in range(width):  
        new_row = []
        for j in range(height):
            new_row.append(board[j][i])
        new_board.append(new_row)
    return new_board

def leftToRight(board): # diagonal 2
    
    height = len(board)
    width = len(board[0])
    new_board = []
    for i in range(width):
        new_row = []
        for j in range(height):
            new_row.append(board[height - 1 - j][width - 1 - i])
        new_board.append(new_row)
    return new_board

def main():
    
    board_str, width, height = input()
    board = makeInto2D(board_str, width, height)
    results = set()

    transforms = [identity, rotate180, horizontalR, verticalR, rotate90, rotate270, rightToLeft, leftToRight]


    for transform in transforms:
        transformed = transform(board)
        results.add(boardToStr(transformed))

    results = [*{*results}]
    for sym in results:
        print(sym)
if __name__ == '__main__':
    main()
#Arrush Shah, pd 4, 2026