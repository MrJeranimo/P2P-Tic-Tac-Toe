import socket


board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
turn = True
turnNum = 1


def TCPHost():
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind(('localhost', 12345))
    host_socket.listen(1)
    client_socket, address = host_socket.accept()
    while True:
        message = host_socket.recv(4096)
        print(message.decode())
        break


def TCPClient():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('localhost', 54321))
    client_socket.connect(('localhost', 12345))
    while True:
        message = "Hello!"
        client_socket.send(message.encode())
        print("Message sent")
        break


def printBoard():
    row = 0
    print()
    while row < 3:
        tiles = board[row]
        if (row != 2):
            print(f" {tiles[0]} | {tiles[1]} | {tiles[2]} ")
            print("---|---|---")
        else:
            print(f" {tiles[0]} | {tiles[1]} | {tiles[2]} ")
            print()
        row += 1


def getInput(identifier):
    while True:
        try:
            num = int(input(f"Enter a {identifier}: "))
            test = board[num]
            return num
        except Exception:
            printBoard()
            print("Input must be between 0-2")


def nextTurn():
    global turn
    global turnNum
    symbol = " "
    if turn:
        symbol = "X"
        turn = False
    else:
        symbol = "O"
        turn = True
    print(f"Player {turn}'s turn")
    row = getInput("row")
    column = getInput("column")
    while board[row][column] != " ":
        printBoard()
        print("Cannot go there")
        row = getInput("row")
        column = getInput("column")
    board[row][column] = symbol
    turnNum += 1


def checkWin():
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return True
    column = 0
    while column < 3:
        if board[0][column] == board[1][column] == board[2][column] != " ":
            return True
        column += 1
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True
    return False


def TicTacToe():
    while True:
        printBoard()
        nextTurn()
        if checkWin():
            printBoard()
            print(f"Game over, Player {turn} wins!")
            break
        if turnNum > 9:
            printBoard()
            print("Game Over, no one won")
            break


def main():
    TicTacToe()
    """print("Enter 0 or 1")
    num = input()
    num = int(num)
    if (num == 0):
        print("Hosting....")
        TCPHost()
    elif (num == 1):
        print("Connecting...")
        TCPClient()"""


if __name__ == "__main__":
    main()
