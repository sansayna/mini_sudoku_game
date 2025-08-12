#!/usr/bin/env python3
# Mini Sudoku (4x4) – CLI Game
# Author: Your Name
# License: MIT
#
# Play a 4x4 Sudoku in the terminal. Commands:
#   - enter moves as: row col val   (all 1-4)
#   - 'hint'      : fill a single correct cell
#   - 'check'     : validate current board
#   - 'solve'     : auto-solve the puzzle
#   - 'reset'     : reset to puzzle start
#   - 'new'       : generate a new puzzle
#   - 'help'      : show help
#   - 'q' or 'quit': exit
#
# Rows and columns are 1-indexed. Only digits 1-4 are allowed.

import random
import copy
import sys
from typing import List, Tuple, Optional

Board = List[List[int]]

def print_board(board: Board):
    """Pretty-print the 4x4 board."""
    horiz = "+---+---+---+---+"
    print("    c1  c2  c3  c4")
    print("  " + horiz)
    for r, row in enumerate(board, start=1):
        line = []
        for c, val in enumerate(row, start=1):
            cell = str(val) if val != 0 else "."
            line.append(f" {cell} ")
        print(f"r{r} |" + "|".join(line) + "|")
        print("  " + horiz)

def is_valid(board: Board, r: int, c: int, val: int) -> bool:
    """Check if placing val at (r,c) follows Sudoku rules (4x4)."""
    # Row and column checks
    if any(board[r][j] == val for j in range(4)): return False
    if any(board[i][c] == val for i in range(4)): return False
    # 2x2 box
    br, bc = (r // 2) * 2, (c // 2) * 2
    for i in range(br, br + 2):
        for j in range(bc, bc + 2):
            if board[i][j] == val:
                return False
    return True

def find_empty(board: Board) -> Optional[Tuple[int, int]]:
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_backtrack(board: Board) -> bool:
    """Solve board in-place using backtracking. Returns True if solved."""
    empty = find_empty(board)
    if not empty:
        return True
    r, c = empty
    nums = [1, 2, 3, 4]
    random.shuffle(nums)
    for val in nums:
        if is_valid(board, r, c, val):
            board[r][c] = val
            if solve_backtrack(board):
                return True
            board[r][c] = 0
    return False

def count_solutions(board: Board, limit: int = 2) -> int:
    """Count solutions up to 'limit' using backtracking. Prunes after limit."""
    empty = find_empty(board)
    if not empty:
        return 1
    r, c = empty
    total = 0
    for val in [1, 2, 3, 4]:
        if is_valid(board, r, c, val):
            board[r][c] = val
            total += count_solutions(board, limit)
            board[r][c] = 0
            if total >= limit:
                break
    return total

def generate_full_solution() -> Board:
    board = [[0] * 4 for _ in range(4)]
    solve_backtrack(board)
    return board

def generate_puzzle(removals: int = 6) -> Tuple[Board, Board]:
    """Generate a 4x4 Sudoku with a unique solution. Returns (puzzle, solution)."""
    solution = generate_full_solution()
    puzzle = copy.deepcopy(solution)

    # Candidate positions to remove
    cells = [(i, j) for i in range(4) for j in range(4)]
    random.shuffle(cells)

    removed = 0
    for (i, j) in cells:
        if removed >= removals:
            break
        temp = puzzle[i][j]
        puzzle[i][j] = 0
        test = copy.deepcopy(puzzle)
        sols = count_solutions(test, limit=2)
        if sols != 1:
            # not uniquely solvable, revert removal
            puzzle[i][j] = temp
        else:
            removed += 1

    return puzzle, solution

def board_complete(board: Board) -> bool:
    return all(all(val != 0 for val in row) for row in board)

def board_valid(board: Board) -> bool:
    """Check if board adheres to Sudoku constraints (ignores zeros)."""
    # Rows
    for i in range(4):
        seen = set()
        for j in range(4):
            v = board[i][j]
            if v == 0: continue
            if v in seen: return False
            seen.add(v)
    # Cols
    for j in range(4):
        seen = set()
        for i in range(4):
            v = board[i][j]
            if v == 0: continue
            if v in seen: return False
            seen.add(v)
    # Boxes
    for br in range(0, 4, 2):
        for bc in range(0, 4, 2):
            seen = set()
            for i in range(br, br+2):
                for j in range(bc, bc+2):
                    v = board[i][j]
                    if v == 0: continue
                    if v in seen: return False
                    seen.add(v)
    return True

HELP = """\
Commands:
  row col val   -> Place value (1-4) at row,col (both 1-4). Example: 2 3 4
  hint          -> Fill one random correct empty cell
  check         -> Validate current board (no rule violations)
  solve         -> Auto-solve and display the solution
  reset         -> Reset the puzzle to its original state
  new           -> Generate a new puzzle
  help          -> Show this help screen
  q / quit      -> Exit the game
"""

def play():
    print("Mini Sudoku (4x4) — Python CLI Game")
    print("Generate a puzzle and start playing. Type 'help' for commands.\n")

    puzzle, solution = generate_puzzle(removals=6)
    start_state = copy.deepcopy(puzzle)
    current = copy.deepcopy(puzzle)

    while True:
        print_board(current)
        if board_complete(current) and current == solution:
            print("🎉 Congratulations! You solved the puzzle!\n")
        cmd = input("> ").strip().lower()

        if cmd in ("q", "quit"):
            print("Goodbye!")
            break
        if cmd == "help":
            print(HELP)
            continue
        if cmd == "new":
            puzzle, solution = generate_puzzle(removals=6)
            start_state = copy.deepcopy(puzzle)
            current = copy.deepcopy(puzzle)
            print("New puzzle generated.\n")
            continue
        if cmd == "reset":
            current = copy.deepcopy(start_state)
            print("Board reset to the starting puzzle.\n")
            continue
        if cmd == "check":
            print("Board is valid." if board_valid(current) else "There are rule violations.")
            continue
        if cmd == "solve":
            current = copy.deepcopy(solution)
            print("Here is the solved board.\n")
            continue
        if cmd == "hint":
            # Find an empty cell and fill with the solution's value
            empties = [(i, j) for i in range(4) for j in range(4) if current[i][j] == 0]
            if not empties:
                print("No empty cells to hint.")
                continue
            i, j = random.choice(empties)
            current[i][j] = solution[i][j]
            print(f"Hint: Filled r{i+1} c{j+1} with {solution[i][j]}.\n")
            continue

        # Try to parse move: "r c v"
        parts = cmd.split()
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            r, c, v = map(int, parts)
            if not (1 <= r <= 4 and 1 <= c <= 4 and 1 <= v <= 4):
                print("Rows, columns, and values must be 1–4.")
                continue
            # Prevent changing given clues
            if start_state[r-1][c-1] != 0:
                print("That cell is fixed in the puzzle and cannot be changed.")
                continue
            # Validate move
            if is_valid(current, r-1, c-1, v):
                current[r-1][c-1] = v
            else:
                print("Invalid move: violates Sudoku rules.")
            continue

        print("Unrecognized command. Type 'help' for options.")

if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\nExiting. Bye!")
