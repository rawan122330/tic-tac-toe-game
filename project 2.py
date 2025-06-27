import tkinter as tk
from tkinter import messagebox
import random
import copy

board = {str(i): ' ' for i in range(1, 10)}
player_symbol = 'X'
computer_symbol = 'O'
player_turn = True
vs_computer = True
buttons = {}

def is_winner(brd, sym):
    wins = [(1,2,3), (4,5,6), (7,8,9), (1,4,7), (2,5,8), (3,6,9), (1,5,9), (3,5,7)]
    return any(brd[str(x)] == brd[str(y)] == brd[str(z)] == sym for x, y, z in wins)

def is_draw(brd):
    return all(value != ' ' for value in brd.values())

def get_best_move(sym):
    temp = copy.deepcopy(board)
    for i in range(1, 10):
        if temp[str(i)] == ' ':
            temp[str(i)] = sym
            if is_winner(temp, sym):
                return str(i)
            temp[str(i)] = ' '
    opponent = player_symbol if sym == computer_symbol else computer_symbol
    for i in range(1, 10):
        if temp[str(i)] == ' ':
            temp[str(i)] = opponent
            if is_winner(temp, opponent):
                return str(i)
            temp[str(i)] = ' '
    if temp['5'] == ' ':
        return '5'
    for i in ['1', '3', '7', '9']:
        if temp[i] == ' ':
            return i
    for i in ['2', '4', '6', '8']:
        if temp[i] == ' ':
            return i

def make_move(pos, sym):
    if board[pos] == ' ':
        board[pos] = sym
        buttons[pos].config(text=sym, state='disabled')
        if sym == 'X':
            buttons[pos].config(fg='black')
        else:
            buttons[pos].config(fg='blue')
        if is_winner(board, sym):
            messagebox.showinfo("Game Over", f"{sym} wins!")
            ask_restart()
        elif is_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            ask_restart()
        return True
    return False

def on_click(pos):
    global player_turn
    if not start_var.get() == "Yes":
        return
    if make_move(pos, player_symbol):
        if vs_computer:
            window.after(400, computer_move)
        else:
            switch_turn()

def computer_move():
    move = get_best_move(computer_symbol)
    make_move(move, computer_symbol)

def switch_turn():
    global player_symbol, computer_symbol
    player_symbol, computer_symbol = computer_symbol, player_symbol

def ask_restart():
    if messagebox.askyesno("Restart", "Do you want to play again?"):
        reset_game()
    else:
        window.quit()

def reset_game():
    global board
    board = {str(i): ' ' for i in range(1, 10)}
    for btn in buttons.values():
        btn.config(text=' ', state='normal', fg='black')

def start_game():
    global vs_computer, player_symbol, computer_symbol
    vs_computer = (mode_var.get() == "Computer")
    player_symbol = symbol_var.get()
    computer_symbol = 'O' if player_symbol == 'X' else 'X'
    reset_game()

# GUI Setup
window = tk.Tk()
window.title("Tic-Tac-Toe")
window.geometry("420x520")  # Wider frame

top_frame = tk.Frame(window)
top_frame.pack(pady=10)

control_frame = tk.Frame(top_frame)
control_frame.pack()

# Play With
tk.Label(control_frame, text="Play With : ").pack(anchor='w', pady=(0, 2))
mode_var = tk.StringVar(value="Computer")
tk.Radiobutton(control_frame, text="Computer", variable=mode_var, value="Computer").pack(anchor='w')
tk.Radiobutton(control_frame, text="Player 2", variable=mode_var, value="Player 2").pack(anchor='w')

tk.Label(control_frame, text="").pack(pady=4)  # Spacer

# Select Symbol
tk.Label(control_frame, text="Select : ").pack(anchor='w', pady=(0, 2))
symbol_var = tk.StringVar(value="X")
tk.Radiobutton(control_frame, text="X", variable=symbol_var, value="X").pack(anchor='w')
tk.Radiobutton(control_frame, text="O", variable=symbol_var, value="O").pack(anchor='w')

tk.Label(control_frame, text="").pack(pady=4)  # Spacer

# Start the game
tk.Label(control_frame, text="Start the game ? ").pack(anchor='w', pady=(0, 2))
start_var = tk.StringVar(value="Yes")
tk.Radiobutton(control_frame, text="Yes", variable=start_var, value="Yes").pack(anchor='w')
tk.Radiobutton(control_frame, text="No", variable=start_var, value="No").pack(anchor='w')

# Start Button (Centered under all options)
tk.Button(top_frame, text="start", command=start_game).pack(pady=10)

# Game Board
board_frame = tk.Frame(window, padx=10, pady=10)
board_frame.pack()

for i in range(3):
    for j in range(3):
        pos = str(3 * i + j + 1)
        btn = tk.Button(board_frame, text=' ', font=('Arial', 24), width=4, height=2, bg='gray',
                        command=lambda p=pos: on_click(p))
        btn.grid(row=i, column=j, padx=2, pady=2)
        buttons[pos] = btn

window.mainloop()