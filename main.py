# Imports the socket module to use a TCP connection
import socket


# Initializes the necessary global variables for the program
board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]  # Game Board
player = "1"         # Player number
otherPlayer = "2"    # Other play number
turn = True          # Is it your turn
turnNum = 1          # Game turn number
symbol = "X"         # Symbol for your turn
otherSymbol = "O"    # Symbol for the other player's turn
winner = ""          # The winner


# Function that creates the TCP host and starts running TicTacToe
def TCPHost():
    # Try-Except statement to prevent run-time connection errors
    try:
        # Creates and binds a TCP socket
        host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        yourIP = input("Enter your IPv4 address: ")
        host_socket.bind((yourIP, 12345))

        # Listens for a connection to the socket
        host_socket.listen(1)
        print("Waiting for a connection...")

        # Accepts the connection and prints the address of the connection
        client_socket, address = host_socket.accept()
        print(f"Connection with {address} established!")

        # Calls the TicTacToe function and passes in the client socket
        TicTacToe(client_socket)

        # Closes all the sockets and stops running once the game is over
        client_socket.close()
        host_socket.close()
        print("All sockets closed")

    # Exception statement to catch connection failures
    except Exception:
        # Closes all the sockets and stops running
        host_socket.close()
        client_socket.close()
        print("Error in game connection. Shutting down...")


# Function that creates the TCP client and starts running TicTacToe
def TCPClient():
    # Try-Except statement to prevent run-time connection errors
    try:
        # Required Global variables statements
        global turn
        global symbol
        global otherSymbol
        global player
        global otherPlayer

        # Updating the initialized variables for player 2
        turn = False
        symbol = "O"
        otherSymbol = "X"
        player = "2"
        otherPlayer = "1"

        # Creates and binds a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        yourIP = input("Enter your IPv4 address: ")
        client_socket.bind((yourIP, 54321))

        # Connects the client to the host
        IP = input("Input the IPv4 address you want to connect to: ")
        client_socket.connect((IP, 12345))
        print("Connected!")

        # Calls TicTacToe and passes in client socket
        TicTacToe(client_socket)

        # Closes the socket and stops running once the game is over
        client_socket.close()
        print("All sockets closed")

    # Exception statement to prevent connection failures
    except Exception:
        # Closes the original socket
        client_socket.close()

        # Prints a generic error message and prompts user input to try again
        answer = input("Error in connection. Try Again? (y/n) ")
        if answer == "y":
            # Runs TCPClient again to try and reconnect/connect
            TCPClient()
        elif answer == "n":
            print("Shutting down...")
        else:
            print("Input not valid, shutting down...")


# Function to receive data across the given socket
# The parameter 'soc' is a socket
# returns the action in string format
def recieveData(soc):
    # Receives, decodes, and returns the data from the socket
    action = soc.recv(4096).decode()
    return action


# Function to send data across the given socket
# The parameter 'soc' is a socket
def sendData(soc, action):
    soc.sendall(action.encode())


# Function to print the board to the terminal
def printBoard():
    row = 0    # Row counter
    print()
    while row < 3:
        # Gets the array corresponding to row number
        tiles = board[row]

        # Prints the row with a '---' after it except the last row
        if (row != 2):
            print(f" {tiles[0]} | {tiles[1]} | {tiles[2]} ")
            print("---|---|---")
        else:
            print(f" {tiles[0]} | {tiles[1]} | {tiles[2]} ")
            print()
        row += 1


# Function to get the input of the user and check if it is valid
# The parameter 'identifier' is either "row" or "column"
def getInput(identifier):
    while True:
        # Try-except statement to prevent invalid input errors
        try:
            num = int(input(f"Enter a {identifier}: "))

            # Tests num to make sure it is valid and won't give an exception
            identifier = board[num]
            return num
        except Exception:
            printBoard()
            print("Input must be between 0-2")


# Function to proceed with the player's next turn
# The parameter 'soc' is a socket
def nextTurn(soc):
    # Required Global variables statements
    global turnNum
    global symbol
    global player

    # Prompts player for their input for their turn
    print("Your turn")
    row = getInput("row")
    column = getInput("column")

    # Checks to make sure spot on board is empty/not taken
    while board[row][column] != " ":
        printBoard()
        print("Cannot go there")
        row = getInput("row")
        column = getInput("column")

    # Adds the symbol of the player to the chosen spot on the board
    board[row][column] = symbol
    turnNum += 1

    # To send the other player the data
    sendData(soc, f"{player},{row},{column}")


# Function for proceeding with the other player's turn
# The parameter 'soc' is a socket
def recvTurn(soc):
    # Required Global variables statements
    global turnNum
    global otherSymbol
    global player

    # Recieves the verified turn data from the other player
    action = recieveData(soc)

    # Splits the data into 3 usable integer variables
    player, row, column = map(int, action.split(","))

    # Adds the symbol of the other player to the chosen spot on the board
    board[row][column] = otherSymbol

    # Tells the player the other player's action
    print(f"Player {player} went in row {row}, column {column}.")
    turnNum += 1


# Function to check if a player won
# returns a boolean
def checkWin():
    # Required Global variables statements
    global winner
    global otherPlayer

    # Loop to check for row victories
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            if turn:
                winner = player
            else:
                winner = otherPlayer
            return True

    # Loop to check for column victories
    column = 0
    while column < 3:
        if board[0][column] == board[1][column] == board[2][column] != " ":
            if turn:
                winner = player
            else:
                winner = otherPlayer
            return True
        column += 1

    # Checks for diagonal victories
    if board[0][0] == board[1][1] == board[2][2] != " ":
        if turn:
            winner = player
        else:
            winner = otherPlayer
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        if turn:
            winner = player
        else:
            winner = otherPlayer
        return True

    # returns false if no victory
    return False


# Function for running Tic Tac Toe
# The parameter 'soc' is a socket
def TicTacToe(soc):
    # Required Global variables statements
    global winner
    global turn

    # Loops till a winner or tie is decided
    while True:
        printBoard()

        # If it is your turn, call nextTurn, else call recvTurn
        if turn:
            nextTurn(soc)
        else:
            print("Waiting for other player...")
            recvTurn(soc)

        # Calls checkWin and prints the winner if true
        if checkWin():
            printBoard()
            print(f"Game over, Player {winner} wins!")
            break

        # Checks if game has exceeded 9 turns in which a draw will be called
        if turnNum > 9:
            printBoard()
            print("Game Over, no one won")
            break

        # Changes the turn for the player
        turn = not turn


# Main function to properly start the program
def main():
    # Prompts user to choose either hosting or connecting to a host
    num = int(input("Enter 0 (Host) or 1 (Connect) "))

    # Calls respective TCP socket functions based on input
    if (num == 0):
        print("Hosting....")
        TCPHost()
    elif (num == 1):
        print("Connecting...")
        TCPClient()


# If statement to make sure only 'main()' is initially run
if __name__ == "__main__":
    main()
