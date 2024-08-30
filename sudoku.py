import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont
import random
import copy

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def remove_numbers(board, num_holes):
    while num_holes > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            num_holes -= 1

def generate_sudoku(num_holes=40):
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)
    remove_numbers(board, num_holes)
    return board

def draw_sudoku_image(board, filename="sudoku.png"):
    image = Image.new("RGB", (450, 450), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 24)

    for i in range(10):
        line_width = 5 if i % 3 == 0 else 2
        draw.line([(i * 50, 0), (i * 50, 450)], fill=(0, 0, 0), width=line_width)
        draw.line([(0, i * 50), (450, i * 50)], fill=(0, 0, 0), width=line_width)

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                x = j * 50 + 20
                y = i * 50 + 10
                draw.text((x, y), str(board[i][j]), fill=(0, 0, 0), font=font)

    image.save(filename)
    return filename

def display_sudoku(board):
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            if board[i][j] == 0:
                entry.delete(0, tk.END)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(board[i][j]))

def generate_and_display():
    try:
        num_holes = int(difficulty_entry.get()) if difficulty_entry.get().isdigit() else difficulty_slider.get()
        board = generate_sudoku(num_holes)
        global current_board, previous_board
        previous_board = copy.deepcopy(current_board)
        current_board = board
        display_sudoku(board)
    except ValueError:
        messagebox.showerror("输入错误", "请输入一个有效的数字")

def solve_sudoku():
    solve(current_board)
    display_sudoku(current_board)

def save_sudoku_image():
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if filepath:
        draw_sudoku_image(current_board, filename=filepath)
        messagebox.showinfo("保存成功", f"数独图片已保存为 {filepath}")

def revert_to_previous():
    global current_board
    if previous_board:
        current_board = copy.deepcopy(previous_board)
        display_sudoku(current_board)
    else:
        messagebox.showinfo("提示", "没有上一题可返回")

# 初始化GUI
root = tk.Tk()
root.title("数独生成器")

# 数独网格显示
entries = [[tk.Entry(root, width=2, font=("Arial", 18), justify="center") for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entries[i][j].grid(row=i, column=j, padx=2, pady=2)

# 滑动条来控制难度
difficulty_label = tk.Label(root, text="选择难度（移除的数字数量）:")
difficulty_label.grid(row=9, column=0, columnspan=4)

difficulty_slider = tk.Scale(root, from_=20, to_=60, orient=tk.HORIZONTAL, length=200)
difficulty_slider.grid(row=9, column=4, columnspan=5)

# 手动输入难度
difficulty_entry = tk.Entry(root, width=5)
difficulty_entry.grid(row=10, column=4, columnspan=2)
difficulty_entry.insert(0, "40")

# 按钮生成数独
generate_button = tk.Button(root, text="生成数独", command=generate_and_display)
generate_button.grid(row=11, column=0, columnspan=4)

# 按钮自动解数独
solve_button = tk.Button(root, text="自动解数独", command=solve_sudoku)
solve_button.grid(row=11, column=4, columnspan=2)

# 按钮保存数独图片
save_button = tk.Button(root, text="保存数独图片", command=save_sudoku_image)
save_button.grid(row=11, column=6, columnspan=3)

# 按钮返回上一题
revert_button = tk.Button(root, text="回到上一题", command=revert_to_previous)
revert_button.grid(row=12, column=4, columnspan=3)

# 初始化数独
previous_board = None
current_board = generate_sudoku(40)
display_sudoku(current_board)

# 启动GUI
root.mainloop()
